# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3
import datetime
import json
import hashlib
import hmac
import uuid
import sys
import os
from typing import Any, Dict, Optional, List
from urllib import request, error, parse


class VmsError(Exception):
    """火山引擎语音服务异常类"""
    pass


DEFAULT_HOST = "cloud-vms.volcengineapi.com"
DEFAULT_VERSION = "2022-01-01"
DEFAULT_REGION = "cn-beijing"
DEFAULT_SERVICE = "vms"


def _utc_xdate(dt: Optional[datetime.datetime] = None) -> str:
    if dt is None:
        dt = datetime.datetime.utcnow()
    return dt.strftime("%Y%m%dT%H%M%SZ")


def _sha256_hex(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _hmac_sha256(key: bytes, content: str) -> bytes:
    return hmac.new(key, content.encode("utf-8"), hashlib.sha256).digest()


def _norm_uri(path: str) -> str:
    return parse.quote(path).replace("%2F", "/").replace("+", "%20")


def _norm_query(params: Dict[str, Any]) -> str:
    items = []
    for k in sorted(params.keys()):
        v = str(params[k])
        items.append(
            parse.quote(k, safe="-_.~") + "=" + parse.quote(v, safe="-_.~")
        )
    return "&".join(items).replace("+", "%20")


def _signing_key(sk: str, date: str, region: str, service: str) -> bytes:
    kdate = _hmac_sha256(sk.encode("utf-8"), date)
    kregion = _hmac_sha256(kdate, region)
    kservice = _hmac_sha256(kregion, service)
    return _hmac_sha256(kservice, "request")


def _build_canonical_request(
    method: str,
    path: str,
    query: Dict[str, Any],
    headers: Dict[str, str],
    body: bytes,
):
    body_hash = _sha256_hex(body)
    signed_headers = {}
    for k, v in headers.items():
        if k in ("Content-Type", "Content-Md5", "Host") or k.startswith("X-"):
            signed_headers[k.lower()] = v.strip()
    if "host" in signed_headers:
        v = signed_headers["host"]
        if ":" in v:
            host, port = v.split(":", 1)
            if port in ("80", "443"):
                signed_headers["host"] = host
    signed_headers_str = ""
    for k in sorted(signed_headers.keys()):
        signed_headers_str += f"{k}:{signed_headers[k]}\n"
    signed_headers_keys = ";".join(sorted(signed_headers.keys()))
    canonical_request = "\n".join(
        [
            method,
            _norm_uri(path or "/"),
            _norm_query(query),
            signed_headers_str,
            signed_headers_keys,
            body_hash,
        ]
    )
    return (
        hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        signed_headers_keys,
        body_hash,
    )


def _build_authorization(
    ak: str,
    sk: str,
    region: str,
    service: str,
    xdate: str,
    method: str,
    path: str,
    query: Dict[str, Any],
    headers: Dict[str, str],
    body: bytes,
) -> (str, str):
    date = xdate[:8]
    hashed_req, signed_headers, body_hash = _build_canonical_request(
        method, path, query, headers, body
    )
    credential_scope = "/".join([date, region, service, "request"])
    signing_str = "\n".join(["HMAC-SHA256", xdate, credential_scope, hashed_req])
    key = _signing_key(sk, date, region, service)
    signature = hmac.new(key, signing_str.encode("utf-8"), hashlib.sha256).hexdigest()
    auth = f"HMAC-SHA256 Credential={ak}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    return auth, body_hash


def _signed_post(
    ak: str,
    sk: str,
    host: str,
    action: str,
    version: str,
    body_obj: Dict[str, Any],
    *,
    region: str = DEFAULT_REGION,
    service: str = DEFAULT_SERVICE,
    timeout: int = 10,
    scheme: str = "https",
    path: str = "/",
) -> Dict[str, Any]:
    query = {"Action": action, "Version": version}
    url = f"{scheme}://{host}{path}?{_norm_query(query)}"
    body = json.dumps(body_obj, ensure_ascii=False, separators=(",", ":")).encode(
        "utf-8"
    )
    headers = {"Content-Type": "application/json", "Host": host}
    xdate = _utc_xdate()
    headers["X-Date"] = xdate
    auth, body_hash = _build_authorization(
        ak, sk, region, service, xdate, "POST", path, query, headers, body
    )
    headers["Authorization"] = auth
    req = request.Request(url=url, data=body, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except error.HTTPError as e:
        detail = (
            e.read().decode("utf-8", errors="ignore") if hasattr(e, "read") else ""
        )
        raise VmsError(f"HTTP {e.code}: {detail}") from e
    except error.URLError as e:
        raise VmsError(str(e)) from e
    except json.JSONDecodeError as e:
        raise VmsError("Invalid JSON response") from e


def _signed_post_form(
    ak: str,
    sk: str,
    host: str,
    action: str,
    version: str,
    form_data: Dict[str, Any],
    *,
    region: str = DEFAULT_REGION,
    service: str = DEFAULT_SERVICE,
    timeout: int = 10,
    scheme: str = "https",
    path: str = "/",
) -> Dict[str, Any]:
    query = {"Action": action, "Version": version}
    url = f"{scheme}://{host}{path}?{_norm_query(query)}"
    form_items = []
    for k, v in form_data.items():
        form_items.append(f"{parse.quote(str(k), safe='')}={parse.quote(str(v), safe='')}")
    body = "&".join(form_items).encode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Host": host}
    xdate = _utc_xdate()
    headers["X-Date"] = xdate
    auth, body_hash = _build_authorization(
        ak, sk, region, service, xdate, "POST", path, query, headers, body
    )
    headers["Authorization"] = auth
    req = request.Request(url=url, data=body, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except error.HTTPError as e:
        detail = (
            e.read().decode("utf-8", errors="ignore") if hasattr(e, "read") else ""
        )
        raise VmsError(f"HTTP {e.code}: {detail}") from e
    except error.URLError as e:
        raise VmsError(str(e)) from e
    except json.JSONDecodeError as e:
        raise VmsError("Invalid JSON response") from e


def query_voice_resources(
    ak: str,
    sk: str,
    *,
    host: str = DEFAULT_HOST,
    version: str = DEFAULT_VERSION,
    region: str = DEFAULT_REGION,
    timeout: int = 10,
    scheme: str = "https",
    path: str = "/",
) -> Dict[str, Any]:
    query_params = {"Type": 0, "Limit": 10, "Offset": 0}
    return _signed_post(
        ak, sk, host, "GetVoiceResourceList", version, query_params,
        region=region, timeout=timeout, scheme=scheme, path=path
    )


def query_number_pools(
    ak: str,
    sk: str,
    *,
    host: str = DEFAULT_HOST,
    version: str = DEFAULT_VERSION,
    region: str = DEFAULT_REGION,
    timeout: int = 10,
    scheme: str = "https",
    path: str = "/",
) -> Dict[str, Any]:
    form_data = {
        "SubServiceType": 102,
        "Limit": 5,
        "Offset": 0
    }
    return _signed_post_form(
        ak, sk, host, "NumberPoolList", version, form_data,
        region=region, timeout=timeout, scheme=scheme, path=path
    )


def create_voice_notify(
    ak: str,
    sk: str,
    phone_number: str,
    resource: str,
    number_pool_no: str,
    *,
    type: int = 0,
    single_open_id: Optional[str] = None,
    host: str = DEFAULT_HOST,
    version: str = DEFAULT_VERSION,
    region: str = DEFAULT_REGION,
    timeout: int = 10,
    scheme: str = "https",
    path: str = "/",
) -> Dict[str, Any]:
    if single_open_id is None:
        single_open_id = uuid.uuid4().hex
    
    single_param: Dict[str, Any] = {
        "Phone": phone_number,
        "Resource": resource,
        "NumberPoolNo": number_pool_no,
        "Type": type,
        "SingleOpenId": single_open_id
    }
    
    body_obj = {"List": [single_param]}
    return _signed_post(
        ak, sk, host, "SingleBatchAppend", version, body_obj,
        region=region, timeout=timeout, scheme=scheme, path=path
    )


def get_ak_sk_from_env() -> tuple[str, str]:
    ak = os.getenv('VOLCENGINE_ACCESS_KEY')
    sk = os.getenv('VOLCENGINE_SECRET_KEY')

    
    if not ak or not sk:
        raise VmsError("请设置环境变量 VOLCENGINE_ACCESS_KEY 和 VOLCENGINE_SECRET_KEY")
    
    return ak, sk


if __name__ == "__main__":
    try:
        ak, sk = get_ak_sk_from_env()
    except VmsError as e:
        print(f"[voice-notify ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("[voice-notify ERROR] 请指定命令", file=sys.stderr)
        print("用法:", file=sys.stderr)
        print("  python scripts/voice_notify.py resource                     # 查询语音资源", file=sys.stderr)
        print("  python scripts/voice_notify.py pool                        # 查询号码池", file=sys.stderr)
        print("  python scripts/voice_notify.py send <手机号> <资源Key> <号码池编号>  # 发送语音通知", file=sys.stderr)
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        if command == "resource":
            result = query_voice_resources(ak=ak, sk=sk)
            print(json.dumps(result, ensure_ascii=False))
        elif command == "pool":
            result = query_number_pools(ak=ak, sk=sk)
            print(json.dumps(result, ensure_ascii=False))
        elif command == "send":
            if len(sys.argv) < 5:
                print("[voice-notify ERROR] send命令需要手机号、资源Key和号码池编号", file=sys.stderr)
                print("用法: python scripts/voice_notify.py send <手机号> <资源Key> <号码池编号>", file=sys.stderr)
                sys.exit(1)
            phone_number = sys.argv[2]
            resource_key = sys.argv[3]
            number_pool_no = sys.argv[4]
            result = create_voice_notify(
                ak=ak,
                sk=sk,
                phone_number=phone_number,
                resource=resource_key,
                number_pool_no=number_pool_no
            )
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(f"[voice-notify ERROR] 未知命令: {command}", file=sys.stderr)
            print("可用命令: resource, pool, send", file=sys.stderr)
            sys.exit(1)
    except VmsError as e:
        print(f"[voice-notify ERROR] {str(e)}", file=sys.stderr)
        sys.exit(1)
