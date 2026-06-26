from typing import Dict, Any, Optional
import uuid
import json
import random
from datetime import datetime

class Accepted:
    def __init__(self, payTo: str, amount: str, network: str = "clawtip",
                 asset: str = "clawtip",
                 maxTimeoutSeconds: int = 60, extra: Optional[Dict[str, Any]] = None):
        self.scheme = "exact"
        self.network = network
        self.asset = asset
        self.amount = str(amount)
        self.payTo = payTo
        self.maxTimeoutSeconds = maxTimeoutSeconds
        self.extra = extra or {"name": "FEN(分)", "version": "2"}
        
    def to_dict(self):
        return {
            "scheme": self.scheme,
            "network": self.network,
            "asset": self.asset,
            "amount": self.amount,
            "payTo": self.payTo,
            "maxTimeoutSeconds": self.maxTimeoutSeconds,
            "extra": self.extra
        }

class Authorization:
    def __init__(self, from_address: str, to: str, value: str, nonce: str = ""):
        self.from_address = from_address
        self.to = to
        self.value = str(value)
        self.nonce = nonce if nonce else uuid.uuid4().hex
        
    def to_dict(self):
        return {
            "from": self.from_address,
            "to": self.to,
            "value": self.value,
            "nonce": self.nonce
        }

class Payload:
    def __init__(self, signature: str, authorization: Authorization):
        self.signature = signature
        self.authorization = authorization
        
    def to_dict(self):
        return {
            "signature": self.signature,
            "authorization": self.authorization.to_dict()
        }

class Resource:
    def __init__(self, url: str, description: str, mimeType: str = "application/json"):
        self.url = url
        self.description = description
        self.mimeType = mimeType
        
    def to_dict(self):
        return {
            "url": self.url,
            "description": self.description,
            "mimeType": self.mimeType
        }

class Extensions:
    def __init__(self, orderNo: str, askedContents: str, deviceId: str, skillId: str = "",
                 slug: str = "", encryptedData: str = "", skillVersion: str = "1.0.8"):
        self.orderNo = orderNo
        self.askedContents = askedContents
        self.deviceId = deviceId
        self.skillId = skillId
        self.slug = slug
        self.skillVersion = skillVersion
        self.encryptedData = encryptedData
        
    def to_dict(self):
        d = {
            "orderNo": self.orderNo,
            "askedContents": self.askedContents,
            "deviceId": self.deviceId
        }
        if self.skillId:
            d["skillId"] = self.skillId
        if self.slug:
            d["slug"] = self.slug
        if self.skillVersion:
            d["skillVersion"] = self.skillVersion
        if self.encryptedData:
            d["encryptedData"] = self.encryptedData
        return d

class PaymentRequest:
    def __init__(self, accepted: Accepted, payload: Payload, resource: Resource, extensions: Extensions,
                 systemId: str = "jd-clawtip", systemToken: str = "jd-clawtip",
                 requestTime: Optional[int] = None, requestNo: Optional[str] = None):
        self.x402Version = 2
        self.accepted = accepted
        self.payload = payload
        self.resource = resource
        self.extensions = extensions
        self.systemId = systemId
        self.systemToken = systemToken
        
        now = datetime.now()
        self.requestTime = requestTime if requestTime is not None else "{:.0f}".format(now.timestamp() * 1000)
        
        if requestNo is not None:
            self.requestNo = requestNo
        else:
            random_digits = "".join([str(random.randint(0, 9)) for _ in range(10)])
            self.requestNo = now.strftime("%Y%m%d%H%M%S") + random_digits
        
    def to_dict(self):
        return {
            "x402Version": self.x402Version,
            "accepted": self.accepted.to_dict(),
            "payload": self.payload.to_dict(),
            "resource": self.resource.to_dict(),
            "extensions": self.extensions.to_dict(),
            "systemId": self.systemId,
            "systemToken": self.systemToken,
            "requestTime": self.requestTime,
            "requestNo": self.requestNo
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
