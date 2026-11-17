"""Local security profile v1. Keys and policy are provisioned by the operator."""
import base64
import hashlib
import hmac
import json
import math
import os
import re
from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
import jcs
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False, str_max_length=4096)

def plain(value):
    if is_dataclass(value): return plain(asdict(value))
    if isinstance(value, Enum): return value.value
    if isinstance(value, datetime): return value.isoformat()
    if isinstance(value, dict): return {k: plain(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)): return [plain(v) for v in value]
    return value

def canonical(value):
    value = plain(value)
    def check(v, depth=0):
        if depth > 20: raise ValueError("JSON nesting limit exceeded")
        if isinstance(v, dict):
            if any(not isinstance(k,str) for k in v): raise ValueError("JSON keys must be strings")
            for x in v.values(): check(x,depth+1)
        elif isinstance(v,list):
            for x in v: check(x,depth+1)
        elif isinstance(v,float) and not math.isfinite(v): raise ValueError("Nonfinite number")
        elif isinstance(v,int) and not isinstance(v,bool) and abs(v)>9007199254740991:
            raise ValueError("Integer outside JCS safe range")
        elif v is not None and not isinstance(v,(str,bool,int,float)): raise ValueError("Not JSON")
    check(value)
    result=jcs.canonicalize(value)
    if len(result)>262144: raise ValueError("JSON byte limit exceeded")
    return result

def b64(data): return base64.urlsafe_b64encode(data).rstrip(b"=").decode()
def unb64(data):
    if not isinstance(data,str) or not re.fullmatch(r"[A-Za-z0-9_-]+",data): raise ValueError("Invalid base64url")
    result=base64.urlsafe_b64decode(data+"="*((-len(data))%4))
    if b64(result)!=data: raise ValueError("Noncanonical base64url")
    return result

def event_body(event):
    body=plain(event).copy()
    body.pop("signature",None)
    return body

def sign_event(event, context, private_key, kid):
    """Sign only after constructing the complete event; never copy a signature to new fields."""
    header=b64(canonical({"alg":"EdDSA","typ":"JEP+JWS","kid":kid}))
    payload=b64(canonical({"context":context,"event":event_body(event)}))
    data=f"{header}.{payload}"
    return data+"."+b64(private_key.sign(data.encode("ascii")))

def verify_event(event, context, trusted_keys=None):
    body=plain(event)
    signature=body.get("signature")
    try:
        if not isinstance(signature,str) or len(signature)>400000: return False
        head,payload,sig=signature.split(".")
        header=json.loads(unb64(head))
        if set(header)!={"alg","typ","kid"} or header["alg"]!="EdDSA" or header["typ"]!="JEP+JWS": return False
        keys=trusted_keys if trusted_keys is not None else json.loads(os.environ.get("JEP_TRUSTED_KEYS","{}"))
        key=unb64(keys[body["issuer"]][header["kid"]])
        expected=canonical({"context":context,"event":event_body(body)})
        if not hmac.compare_digest(unb64(payload),expected): return False
        Ed25519PublicKey.from_public_bytes(key).verify(unb64(sig),f"{head}.{payload}".encode("ascii"))
        return True
    except Exception:
        return False

def principal(request: Request):
    config=json.loads(os.environ.get("JEP_CLIENTS","{}"))
    if not config: raise HTTPException(503,"API authentication is not configured")
    auth=request.headers.get("authorization","")
    if not auth.startswith("Bearer ") or len(auth)<39: raise HTTPException(401,"Bearer token required")
    digest=hashlib.sha256(auth[7:].encode()).hexdigest()
    client=next((v for k,v in config.items() if hmac.compare_digest(k,digest)),None)
    if not client or not client.get("tenant"): raise HTTPException(401,"Invalid token")
    return client

def require(client, permission, issuer=None):
    if permission not in client.get("permissions",[]): raise HTTPException(403,"Permission denied")
    if issuer is not None and issuer not in client.get("issuers",[]): raise HTTPException(403,"Issuer is not assigned to caller")

class BodyLimit:
    def __init__(self,app): self.app=app
    async def __call__(self,scope,receive,send):
        if scope["type"]!="http": return await self.app(scope,receive,send)
        chunks=[]; size=0
        while True:
            message=await receive()
            if message["type"]=="http.disconnect": return
            size+=len(message.get("body",b""))
            if size>262144:
                return await JSONResponse({"detail":"Body too large"},413)(scope,receive,send)
            chunks.append(message)
            if not message.get("more_body",False): break
        async def replay():
            if chunks: return chunks.pop(0)
            return await receive()
        await self.app(scope,replay,send)

def harden(app):
    app.add_middleware(BodyLimit)
    @app.exception_handler(ValueError)
    async def invalid(request,exc): return JSONResponse({"detail":str(exc)},422)
    @app.exception_handler(OverflowError)
    async def full(request,exc): return JSONResponse({"detail":"Capacity exceeded"},429)
