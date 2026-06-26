#!/usr/bin/env python3
import argparse
import base64
import hashlib
import hmac
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from difflib import SequenceMatcher
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_ALIAS_FILE = ROOT_DIR / "references" / "resource_aliases.json"
BROWSER_CAPTURE_SCRIPT = ROOT_DIR / "scripts" / "browser_capture.mjs"
RSA_KEY_SEPARATOR = base64.urlsafe_b64encode(b"-pk_separator-").decode("ascii")


class ApiError(Exception):
    def __init__(self, message, method, url, status_code=None, body=""):
        super().__init__(message)
        self.method = method
        self.url = url
        self.status_code = status_code
        self.body = body


def print_json(data, code):
    print(json.dumps(data, ensure_ascii=False, indent=2))
    sys.exit(code)


def error_to_dict(stage, err, extra=None):
    payload = {
        "ok": False,
        "stage": stage,
        "error": str(err),
    }
    if isinstance(err, ApiError):
        payload.update({
            "method": err.method,
            "url": err.url,
            "status_code": err.status_code,
            "response_body": err.body,
        })
    if extra:
        payload.update(extra)
    return payload


def load_dotenv(path):
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or key in os.environ:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ[key] = value


def normalize(text):
    text = (text or "").strip().lower()
    text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    text = re.sub(r"\s+", "", text)
    return re.sub(r"[()（）【】\[\]{}·,，。.:：!！?？'\"-_/\\]", "", text)


def load_aliases(path):
    alias_file = Path(path)
    if not alias_file.exists():
        return {}
    with alias_file.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def flatten_tree(nodes, result=None):
    result = result or []
    for node in nodes or []:
        result.append({
            "id": node.get("id"),
            "name": node.get("name", ""),
            "leaf": bool(node.get("leaf", False)),
            "type": node.get("type"),
        })
        flatten_tree(node.get("children") or [], result)
    return result


def flatten_org_tree(nodes, result=None):
    result = result or []
    for node in nodes or []:
        children = node.get("children") or []
        result.append({
            "id": node.get("id"),
            "name": node.get("name", ""),
            "create_time": node.get("createTime"),
            "read_only": node.get("readOnly"),
            "leaf": len(children) == 0,
        })
        flatten_org_tree(children, result)
    return result


def extract_response_data(payload, stage):
    if isinstance(payload, dict):
        if payload.get("code") not in (None, 0):
            raise ValueError(f"{stage}接口返回失败: code={payload.get('code')}, msg={payload.get('msg')}")
        return payload.get("data")
    return payload


def extract_tree_nodes(payload):
    data = extract_response_data(payload, "资源树")
    if isinstance(data, list):
        return data
    raise ValueError("资源树接口返回格式不符合预期，未找到 data 列表")


def base64url(raw):
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def sign_jwt(payload, secret_key):
    header = {"alg": "HS256", "typ": "JWT"}
    header_part = base64url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_part = base64url(json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    signing_input = f"{header_part}.{payload_part}".encode("ascii")
    signature = hmac.new(secret_key.encode("utf-8"), signing_input, hashlib.sha256).digest()
    return f"{header_part}.{payload_part}.{base64url(signature)}"


def aes_cipher_name(secret_key):
    length = len(secret_key.encode("utf-8"))
    if length == 16:
        return "aes-128-cbc"
    if length == 24:
        return "aes-192-cbc"
    if length == 32:
        return "aes-256-cbc"
    raise ValueError("Secret Key 长度必须是 16、24 或 32 字节")


def aes_encrypt(plain_text, secret_key, iv):
    if shutil.which("openssl") is None:
        raise RuntimeError("当前环境缺少 openssl 命令，无法生成鉴权签名")
    if len(iv.encode("utf-8")) != 16:
        raise ValueError("Access Key 长度必须是 16 字节，才能作为 AES IV")

    cmd = [
        "openssl",
        "enc",
        f"-{aes_cipher_name(secret_key)}",
        "-base64",
        "-A",
        "-nosalt",
        "-K",
        secret_key.encode("utf-8").hex(),
        "-iv",
        iv.encode("utf-8").hex(),
    ]
    proc = subprocess.run(cmd, input=plain_text.encode("utf-8"), capture_output=True, check=False)
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(stderr or "openssl 加密失败")
    return proc.stdout.decode("utf-8").strip()


def build_ask_auth(access_key, secret_key):
    source = f"{access_key}|{uuid.uuid4()}|{int(time.time() * 1000)}"
    signature = aes_encrypt(source, secret_key, access_key)
    token = sign_jwt({"accessKey": access_key, "signature": signature}, secret_key)
    return {
        "access_key": access_key,
        "signature": signature,
        "x_de_ask_token": token,
    }


def build_headers(ask_auth):
    return {
        "Accept": "application/json;charset=UTF-8",
        "Content-Type": "application/json",
        "accessKey": ask_auth["access_key"],
        "signature": ask_auth["signature"],
        "X-DE-ASK-TOKEN": ask_auth["x_de_ask_token"],
    }


def build_switch_headers(ask_auth):
    return {
        "Accept": "application/json;charset=UTF-8",
        "Content-Type": "application/json",
        "X-DE-ASK-TOKEN": ask_auth["x_de_ask_token"],
    }


def build_token_headers(x_de_token):
    return {
        "Accept": "application/json;charset=UTF-8",
        "Content-Type": "application/json",
        "X-DE-TOKEN": x_de_token,
    }


def get_header(headers, name, default=None):
    target = name.lower()
    for key, value in headers.items():
        if key.lower() == target:
            return value
    return default


def post_json(url, payload, headers, timeout=60):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    forwarded_headers = dict(headers)
    forwarded_headers.setdefault("X-Forwarded-Uri", urlparse(url).path)
    forwarded_headers.setdefault("X-Forwarded-Method", "POST")
    request = Request(url, data=data, headers=forwarded_headers, method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, dict(response.headers), response.read()
    except HTTPError as err:
        body = err.read().decode("utf-8", errors="replace")
        raise ApiError(str(err), "POST", url, err.code, body)
    except URLError as err:
        raise ApiError(str(err), "POST", url, None, "")


def get_bytes(url, headers=None, timeout=60):
    request = Request(url, headers=dict(headers or {}), method="GET")
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, dict(response.headers), response.read()
    except HTTPError as err:
        body = err.read().decode("utf-8", errors="replace")
        raise ApiError(str(err), "GET", url, err.code, body)
    except URLError as err:
        raise ApiError(str(err), "GET", url, None, "")


def request_with_fallback(base_url, method, paths, payload=None, headers=None, timeout=60):
    last_error = None
    for path in paths:
        url = f"{base_url.rstrip('/')}{path}"
        try:
            if method == "GET":
                return get_bytes(url, headers=headers, timeout=timeout)
            if method == "POST":
                return post_json(url, payload, headers or {}, timeout=timeout)
            raise ValueError(f"不支持的请求方法: {method}")
        except ApiError as err:
            last_error = err
            if err.status_code not in (404, None):
                raise
    if last_error:
        raise last_error
    raise ValueError("未提供可用的请求路径")


def fetch_dekey(base_url):
    _, _, body = request_with_fallback(
        base_url,
        "GET",
        ["/de2api/dekey", "/dekey"],
        headers={"Accept": "application/json;charset=UTF-8"},
        timeout=60,
    )
    payload = json.loads(body.decode("utf-8"))
    data = extract_response_data(payload, "dekey")
    if not isinstance(data, str) or not data:
        raise ValueError("dekey 接口未返回有效字符串")
    return data


def aes_decrypt(cipher_text, secret_key):
    if shutil.which("openssl") is None:
        raise RuntimeError("当前环境缺少 openssl 命令，无法执行账号密码登录加密")
    secret_key_bytes = secret_key.encode("utf-8")
    if len(secret_key_bytes) not in (16, 24, 32):
        raise ValueError("dekey 中的 AES key 长度不合法")

    cmd = [
        "openssl",
        "enc",
        f"-{aes_cipher_name(secret_key)}",
        "-d",
        "-base64",
        "-A",
        "-nosalt",
        "-K",
        secret_key_bytes.hex(),
        "-iv",
        b"0000000000000000".hex(),
    ]
    proc = subprocess.run(cmd, input=cipher_text.encode("utf-8"), capture_output=True, check=False)
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(stderr or "openssl 解密 dekey 失败")
    return proc.stdout.decode("utf-8")


def split_dekey(dekey):
    for separator in (RSA_KEY_SEPARATOR, RSA_KEY_SEPARATOR.rstrip("=")):
        if separator and separator in dekey:
            parts = dekey.split(separator, 1)
            if len(parts) == 2 and parts[0] and parts[1]:
                return parts[0], parts[1]
    raise ValueError("dekey 格式不符合预期，无法解析公钥信息")


def format_public_key(public_key):
    body = "\n".join(public_key[index:index + 64] for index in range(0, len(public_key), 64))
    return f"-----BEGIN PUBLIC KEY-----\n{body}\n-----END PUBLIC KEY-----\n"


def rsa_encrypt(plain_text, public_key):
    if shutil.which("openssl") is None:
        raise RuntimeError("当前环境缺少 openssl 命令，无法执行账号密码登录加密")
    with tempfile.TemporaryDirectory(prefix="dataease-pubkey-") as tmpdir:
        key_path = Path(tmpdir) / "public.pem"
        key_path.write_text(format_public_key(public_key), encoding="utf-8")
        proc = subprocess.run(
            ["openssl", "pkeyutl", "-encrypt", "-pubin", "-inkey", str(key_path)],
            input=plain_text.encode("utf-8"),
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            stderr = proc.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(stderr or "openssl RSA 加密失败")
        return base64.b64encode(proc.stdout).decode("ascii")


def encrypt_login_field(value, dekey):
    encrypted_public_key, aes_key = split_dekey(dekey)
    public_key = aes_decrypt(encrypted_public_key, aes_key).strip()
    if not public_key:
        raise ValueError("dekey 解密后未得到有效公钥")
    return rsa_encrypt(value, public_key)


def login_with_password(base_url, username, password, login_origin):
    dekey = fetch_dekey(base_url)
    payload = {
        "name": encrypt_login_field(username, dekey),
        "pwd": encrypt_login_field(password, dekey),
        "origin": int(login_origin),
    }
    _, _, body = request_with_fallback(
        base_url,
        "POST",
        ["/de2api/login/localLogin", "/login/localLogin"],
        payload=payload,
        headers={"Accept": "application/json;charset=UTF-8", "Content-Type": "application/json"},
        timeout=60,
    )
    result = json.loads(body.decode("utf-8"))
    data = extract_response_data(result, "账号密码登录")
    if not isinstance(data, dict):
        raise ValueError("账号密码登录接口返回格式不符合预期")
    mfa = data.get("mfa") or {}
    if isinstance(mfa, dict) and mfa.get("enabled"):
        raise ValueError("当前账号开启了 MFA，skill 暂不支持 MFA 登录")
    if data.get("invalidPwd"):
        raise ValueError("当前账号需要修改无效密码后才能继续登录")
    token = data.get("token")
    if not token:
        raise ValueError("账号密码登录成功，但接口未返回 token")
    return {
        "auth_mode": "password",
        "x_de_token": token,
        "token_exp": data.get("exp"),
        "login_origin": int(login_origin),
    }


def exchange_de_token(base_url, ask_auth, target_path, payload=None, target_method="POST"):
    url = f"{base_url.rstrip('/')}/de2api/apisix/check"
    headers = build_headers(ask_auth)
    headers["X-Forwarded-Uri"] = target_path
    headers["X-Forwarded-Method"] = target_method
    _, response_headers, _ = post_json(url, payload, headers, timeout=60)
    x_de_token = get_header(response_headers, "X-DE-TOKEN")
    if not x_de_token:
        raise ValueError("apisix/check 未返回 X-DE-TOKEN")
    return x_de_token


def query_org_tree(base_url, headers, keyword="", desc=True):
    url = f"{base_url.rstrip('/')}/de2api/org/page/tree"
    _, _, body = post_json(url, {"keyword": keyword, "desc": bool(desc)}, headers, timeout=60)
    return json.loads(body.decode("utf-8"))


def switch_organization(base_url, headers, org_id):
    url = f"{base_url.rstrip('/')}/de2api/user/switch/{org_id}"
    _, _, body = post_json(url, None, headers, timeout=60)
    return json.loads(body.decode("utf-8"))


def query_resource_tree(base_url, headers, busi_type, resource_table):
    url = f"{base_url.rstrip('/')}/de2api/dataVisualization/tree"
    _, _, body = post_json(
        url,
        {"busiFlag": busi_type, "resourceTable": resource_table},
        headers,
        timeout=60,
    )
    return json.loads(body.decode("utf-8"))


def parse_pixel(pixel_text):
    parts = [part.strip() for part in (pixel_text or "").split("*", 1)]
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("pixel 格式必须是 宽*高，例如 1920*1080")
    try:
        width = int(parts[0])
        height = int(parts[1])
    except ValueError as err:
        raise ValueError("pixel 宽高必须是整数") from err
    if width <= 0 or height <= 0:
        raise ValueError("pixel 宽高必须大于 0")
    return width, height


def build_preview_url(base_url, resource_id, busi_type):
    url = f"{base_url.rstrip('/')}/#/preview?dvId={resource_id}&dvType={busi_type}"
    if (busi_type or "").lower() == "dashboard":
        url += "&report=true"
    return url


def resolve_capture_token(args, auth_context, target_path, target_payload=None):
    request_mode = resolve_request_mode(args)
    if getattr(args, "x_de_token", ""):
        return args.x_de_token, {
            "used_x_de_token": True,
            "used_org_id": "",
            "token_source": "user_supplied",
            "auth_mode": "token",
            "request_mode": request_mode,
        }

    if auth_context.get("auth_mode") == "password":
        base_token = auth_context["x_de_token"]
        if getattr(args, "org_id", ""):
            switch_result = switch_organization(args.base_url, build_token_headers(base_token), args.org_id)
            switch_data = extract_response_data(switch_result, "切换组织")
            x_de_token = switch_data.get("token") if isinstance(switch_data, dict) else None
            if not x_de_token:
                raise ValueError("切换组织接口未返回 data.token")
            return x_de_token, {
                "used_x_de_token": True,
                "used_org_id": str(args.org_id),
                "token_exp": switch_data.get("exp"),
                "token_source": "switched_org",
                "auth_mode": "password",
                "request_mode": request_mode,
            }
        return base_token, {
            "used_x_de_token": True,
            "used_org_id": "",
            "token_exp": auth_context.get("token_exp"),
            "token_source": "password_login",
            "auth_mode": "password",
            "request_mode": request_mode,
        }

    if getattr(args, "org_id", ""):
        if request_mode == "gateway":
            switch_headers = build_headers(auth_context)
        else:
            de_token = exchange_de_token(args.base_url, auth_context, f"/de2api/user/switch/{args.org_id}")
            switch_headers = build_token_headers(de_token)
        switch_result = switch_organization(args.base_url, switch_headers, args.org_id)
        switch_data = extract_response_data(switch_result, "切换组织")
        x_de_token = switch_data.get("token") if isinstance(switch_data, dict) else None
        if not x_de_token:
            raise ValueError("切换组织接口未返回 data.token")
        return x_de_token, {
            "used_x_de_token": True,
            "used_org_id": str(args.org_id),
            "token_exp": switch_data.get("exp"),
            "token_source": "switched_org",
            "auth_mode": "ask_token",
            "request_mode": request_mode,
        }

    x_de_token = exchange_de_token(args.base_url, auth_context, target_path, target_payload)
    return x_de_token, {
        "used_x_de_token": True,
        "used_org_id": "",
        "token_source": "apisix_check",
        "auth_mode": "ask_token",
        "request_mode": request_mode,
    }


def run_browser_capture(preview_url, x_de_token, pixel, ext_wait_time, result_format, output_path):
    if shutil.which("node") is None:
        raise RuntimeError("当前环境缺少 node 命令，无法执行本地浏览器截图")
    if not BROWSER_CAPTURE_SCRIPT.exists():
        raise RuntimeError(f"未找到浏览器截图脚本: {BROWSER_CAPTURE_SCRIPT}")

    width, height = parse_pixel(pixel)
    cmd = [
        "node",
        str(BROWSER_CAPTURE_SCRIPT),
        "--url",
        preview_url,
        "--token",
        x_de_token,
        "--width",
        str(width),
        "--height",
        str(height),
        "--wait-seconds",
        str(ext_wait_time),
        "--result-format",
        str(result_format),
        "--output",
        str(output_path),
    ]
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()
    if proc.returncode != 0:
        detail = stderr or stdout or "浏览器截图失败"
        raise RuntimeError(detail)
    if not output_path.exists():
        raise RuntimeError("浏览器截图命令执行成功，但未生成输出文件")
    if stdout:
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            return {"raw_output": stdout}
    return {}


def score_resource(item, query):
    name = item.get("name", "")
    name_norm = normalize(name)
    query_norm = normalize(query)
    score = SequenceMatcher(None, query_norm, name_norm).ratio()
    if query_norm == name_norm:
        score += 1.0
    elif query_norm and query_norm in name_norm:
        score += 0.25
    if item.get("leaf"):
        score += 0.05
    return score


def search_resources(resources, query, top_n=20):
    scored = []
    for item in resources:
        if not item.get("name"):
            continue
        scored.append((score_resource(item, query), item))
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[:top_n]


def resolve_resource(resources, query, alias_file, min_score):
    aliases = load_aliases(alias_file)
    resolved_query = aliases.get(query, query)
    leaf_resources = [item for item in resources if item.get("leaf")]
    query_norm = normalize(resolved_query)

    exact_matches = [
        item for item in leaf_resources
        if normalize(item.get("name")) == query_norm
    ]
    if len(exact_matches) == 1:
        return {
            "ok": True,
            "resolved_query": resolved_query,
            "resource": exact_matches[0],
            "candidates": [{"score": 2.05, **exact_matches[0]}],
        }, 0
    if len(exact_matches) > 1:
        return {
            "ok": False,
            "stage": "match",
            "error": "存在多个同名资源，无法唯一确定导出目标",
            "query": resolved_query,
            "candidates": [{"score": 2.05, **item} for item in exact_matches],
        }, 2

    candidates = search_resources(leaf_resources, resolved_query, top_n=5)
    if not candidates:
        return {
            "ok": False,
            "stage": "match",
            "error": "资源树中没有找到任何候选资源",
            "query": resolved_query,
        }, 2

    candidate_payload = [
        {
            "score": round(score, 4),
            "id": item.get("id"),
            "name": item.get("name"),
            "leaf": item.get("leaf"),
            "type": item.get("type"),
        }
        for score, item in candidates
    ]
    best_score, best_item = candidates[0]
    second_score = candidates[1][0] if len(candidates) > 1 else None

    if best_score < min_score:
        return {
            "ok": False,
            "stage": "match",
            "error": "没有找到足够可信的匹配结果",
            "query": resolved_query,
            "candidates": candidate_payload,
        }, 2

    if second_score is not None and abs(best_score - second_score) < 0.08:
        return {
            "ok": False,
            "stage": "match",
            "error": "存在多个相似资源，无法安全猜测导出目标",
            "query": resolved_query,
            "candidates": candidate_payload,
        }, 2

    return {
        "ok": True,
        "resolved_query": resolved_query,
        "resource": best_item,
        "candidates": candidate_payload,
    }, 0


def guess_extension(result_format, content_type):
    content_type = (content_type or "").lower()
    if result_format == 1 or "pdf" in content_type:
        return ".pdf"
    return ".jpg"


def load_auth(args):
    if not args.base_url:
        print_json({
            "ok": False,
            "stage": "config",
            "error": "缺少必需配置，请通过命令行参数、系统环境变量或 .env 提供",
            "missing": ["DATAEASE_BASE_URL"],
        }, 1)

    if getattr(args, "x_de_token", ""):
        return {"auth_mode": "token"}

    has_password_auth = bool(args.username or args.password)
    if has_password_auth:
        missing = []
        if not args.username:
            missing.append("DATAEASE_USERNAME")
        if not args.password:
            missing.append("DATAEASE_PASSWORD")
        if missing:
            print_json({
                "ok": False,
                "stage": "config",
                "error": "用户名密码登录配置不完整，请同时提供用户名和密码",
                "missing": missing,
            }, 1)
        try:
            return login_with_password(args.base_url, args.username.strip(), args.password, args.login_origin)
        except Exception as err:
            print_json({"ok": False, "stage": "auth", "error": str(err)}, 1)

    missing = []
    if not args.access_key:
        missing.append("DATAEASE_ACCESS_KEY")
    if not args.secret_key:
        missing.append("DATAEASE_SECRET_KEY")
    if missing:
        missing.extend(["DATAEASE_USERNAME", "DATAEASE_PASSWORD"])
        print_json({
            "ok": False,
            "stage": "config",
            "error": "缺少鉴权配置，请提供 accessKey/secretKey 或 username/password",
            "missing": missing,
        }, 1)

    try:
        ask_auth = build_ask_auth(args.access_key, args.secret_key)
        ask_auth["auth_mode"] = "ask_token"
        return ask_auth
    except Exception as err:
        print_json({"ok": False, "stage": "auth", "error": str(err)}, 1)


def add_common_auth_args(parser):
    parser.add_argument("--base-url", default=os.getenv("DATAEASE_BASE_URL", ""))
    parser.add_argument("--access-key", default=os.getenv("DATAEASE_ACCESS_KEY", ""))
    parser.add_argument("--secret-key", default=os.getenv("DATAEASE_SECRET_KEY", ""))
    parser.add_argument("--username", default=os.getenv("DATAEASE_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("DATAEASE_PASSWORD", ""))
    parser.add_argument("--login-origin", type=int, default=int(os.getenv("DATAEASE_LOGIN_ORIGIN", "0")))
    parser.add_argument("--request-mode", default=os.getenv("DATAEASE_REQUEST_MODE", "auto"), choices=["auto", "gateway", "backend"])


def add_runtime_args(parser):
    parser.add_argument("--org-id", default="")
    parser.add_argument("--x-de-token", default="")


def add_resource_tree_args(parser):
    add_runtime_args(parser)
    parser.add_argument("--busi-type", default="dashboard", choices=["dashboard", "dataV"])
    parser.add_argument("--resource-table", default="core")


def build_parser():
    parser = argparse.ArgumentParser(description="查询 DataEase 组织、资源并导出截图或 PDF")
    subparsers = parser.add_subparsers(dest="command")

    list_orgs = subparsers.add_parser("list-orgs", help="查询组织树")
    add_common_auth_args(list_orgs)
    list_orgs.add_argument("--org-keyword", default="")

    switch_org = subparsers.add_parser("switch-org", help="切换组织并返回 x-de-token")
    add_common_auth_args(switch_org)
    switch_org.add_argument("--org-id", required=True)

    list_resources = subparsers.add_parser("list-resources", help="查询组织下的仪表板或大屏列表")
    add_common_auth_args(list_resources)
    add_resource_tree_args(list_resources)
    list_resources.add_argument("--resource-name", default="")
    list_resources.add_argument("--limit", type=int, default=100)
    list_resources.add_argument("--alias-file", default=str(DEFAULT_ALIAS_FILE))

    capture = subparsers.add_parser("capture", help="导出截图或 PDF")
    add_common_auth_args(capture)
    add_resource_tree_args(capture)
    name_or_id = capture.add_mutually_exclusive_group(required=True)
    name_or_id.add_argument("--resource-name")
    name_or_id.add_argument("--resource-id")
    capture.add_argument("--alias-file", default=str(DEFAULT_ALIAS_FILE))
    capture.add_argument("--min-score", type=float, default=0.55)
    capture.add_argument("--pixel", default="1920*1080")
    capture.add_argument("--ext-wait-time", type=int, default=0)
    capture.add_argument("--result-format", type=int, default=0, choices=[0, 1])
    capture.add_argument("--output-dir", default="outputs")

    return parser


def parse_args():
    parser = build_parser()
    argv = sys.argv[1:]
    commands = {"list-orgs", "switch-org", "list-resources", "capture"}
    if not argv:
        parser.print_help()
        parser.exit(0)
    if argv[0] not in commands and argv[0] not in {"-h", "--help"}:
        argv = ["capture"] + argv
    return parser.parse_args(argv)


def infer_request_mode(base_url):
    port = urlparse(base_url).port
    if port == 8100:
        return "backend"
    return "gateway"


def resolve_request_mode(args):
    if getattr(args, "request_mode", "auto") != "auto":
        return args.request_mode
    return infer_request_mode(args.base_url)


def resolve_runtime_headers(args, auth_context, target_path, target_payload=None):
    request_mode = resolve_request_mode(args)
    if getattr(args, "x_de_token", ""):
        return build_token_headers(args.x_de_token), {
            "used_x_de_token": True,
            "used_org_id": "",
            "token_source": "user_supplied",
            "auth_mode": "token",
            "request_mode": request_mode,
        }

    if auth_context.get("auth_mode") == "password":
        base_token = auth_context["x_de_token"]
        if getattr(args, "org_id", ""):
            switch_result = switch_organization(args.base_url, build_token_headers(base_token), args.org_id)
            switch_data = extract_response_data(switch_result, "切换组织")
            x_de_token = switch_data.get("token") if isinstance(switch_data, dict) else None
            if not x_de_token:
                raise ValueError("切换组织接口未返回 data.token")
            return build_token_headers(x_de_token), {
                "used_x_de_token": True,
                "used_org_id": str(args.org_id),
                "token_exp": switch_data.get("exp"),
                "token_source": "switched_org",
                "auth_mode": "password",
                "request_mode": request_mode,
            }
        return build_token_headers(base_token), {
            "used_x_de_token": True,
            "used_org_id": "",
            "token_exp": auth_context.get("token_exp"),
            "token_source": "password_login",
            "auth_mode": "password",
            "request_mode": request_mode,
        }

    if request_mode == "gateway":
        if getattr(args, "org_id", ""):
            switch_result = switch_organization(args.base_url, build_headers(auth_context), args.org_id)
            switch_data = extract_response_data(switch_result, "切换组织")
            x_de_token = switch_data.get("token") if isinstance(switch_data, dict) else None
            if not x_de_token:
                raise ValueError("切换组织接口未返回 data.token")
            return build_token_headers(x_de_token), {
                "used_x_de_token": True,
                "used_org_id": str(args.org_id),
                "token_exp": switch_data.get("exp"),
                "token_source": "switched_org",
                "auth_mode": "ask_token",
                "request_mode": request_mode,
            }

        return build_headers(auth_context), {
            "used_x_de_token": False,
            "used_org_id": "",
            "token_source": "ask_token",
            "auth_mode": "ask_token",
            "request_mode": request_mode,
        }

    if getattr(args, "org_id", ""):
        de_token = exchange_de_token(args.base_url, auth_context, f"/de2api/user/switch/{args.org_id}")
        switch_result = switch_organization(args.base_url, build_token_headers(de_token), args.org_id)
        switch_data = extract_response_data(switch_result, "切换组织")
        x_de_token = switch_data.get("token") if isinstance(switch_data, dict) else None
        if not x_de_token:
            raise ValueError("切换组织接口未返回 data.token")
        return build_token_headers(x_de_token), {
            "used_x_de_token": True,
            "used_org_id": str(args.org_id),
            "token_exp": switch_data.get("exp"),
            "token_source": "switched_org",
            "auth_mode": "ask_token",
            "request_mode": request_mode,
        }

    de_token = exchange_de_token(args.base_url, auth_context, target_path, target_payload)
    return build_token_headers(de_token), {
        "used_x_de_token": True,
        "used_org_id": "",
        "token_source": "apisix_check",
        "auth_mode": "ask_token",
        "request_mode": request_mode,
    }


def command_list_orgs(args, auth_context):
    try:
        request_payload = {"keyword": args.org_keyword, "desc": True}
        headers, runtime_info = resolve_runtime_headers(args, auth_context, "/de2api/org/page/tree", request_payload)
        org_tree = query_org_tree(args.base_url, headers, args.org_keyword)
        org_data = extract_response_data(org_tree, "组织树")
        organizations = flatten_org_tree(org_data)
        print_json({
            "ok": True,
            "stage": "org_tree",
            "org_keyword": args.org_keyword,
            "organizations": organizations,
            "total": len(organizations),
            **runtime_info,
        }, 0)
    except Exception as err:
        print_json(error_to_dict("org_tree", err, {"base_url": args.base_url}), 1)


def command_switch_org(args, auth_context):
    try:
        request_mode = resolve_request_mode(args)
        if auth_context.get("auth_mode") == "password":
            switch_headers = build_token_headers(auth_context["x_de_token"])
            auth_mode = "password"
        elif request_mode == "gateway":
            switch_headers = build_headers(auth_context)
            auth_mode = "ask_token"
        else:
            de_token = exchange_de_token(args.base_url, auth_context, f"/de2api/user/switch/{args.org_id}")
            switch_headers = build_token_headers(de_token)
            auth_mode = "ask_token"
        switch_result = switch_organization(args.base_url, switch_headers, args.org_id)
        switch_data = extract_response_data(switch_result, "切换组织")
        x_de_token = switch_data.get("token") if isinstance(switch_data, dict) else None
        if not x_de_token:
            raise ValueError("切换组织接口未返回 data.token")
        print_json({
            "ok": True,
            "stage": "switch_org",
            "org_id": str(args.org_id),
            "x_de_token": x_de_token,
            "token_exp": switch_data.get("exp"),
            "token_source": "switched_org",
            "auth_mode": auth_mode,
            "request_mode": request_mode,
        }, 0)
    except Exception as err:
        print_json(error_to_dict("switch_org", err, {"org_id": args.org_id}), 1)


def command_list_resources(args, auth_context):
    try:
        request_payload = {"busiFlag": args.busi_type, "resourceTable": args.resource_table}
        headers, runtime_info = resolve_runtime_headers(args, auth_context, "/de2api/dataVisualization/tree", request_payload)
        resource_tree = query_resource_tree(args.base_url, headers, args.busi_type, args.resource_table)
        resources = [item for item in flatten_tree(extract_tree_nodes(resource_tree)) if item.get("leaf")]

        if args.resource_name:
            aliases = load_aliases(args.alias_file)
            resolved_query = aliases.get(args.resource_name, args.resource_name)
            candidates = [
                {
                    "score": round(score, 4),
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "leaf": item.get("leaf"),
                    "type": item.get("type"),
                }
                for score, item in search_resources(resources, resolved_query, top_n=args.limit)
            ]
            print_json({
                "ok": True,
                "stage": "resource_list",
                "busi_type": args.busi_type,
                "resource_name": args.resource_name,
                "resolved_query": resolved_query,
                "resources": candidates,
                "total": len(candidates),
                **runtime_info,
            }, 0)

        resource_list = sorted(resources, key=lambda item: (item.get("name") or "").lower())[:args.limit]
        print_json({
            "ok": True,
            "stage": "resource_list",
            "busi_type": args.busi_type,
            "resources": resource_list,
            "total": len(resource_list),
            **runtime_info,
        }, 0)
    except Exception as err:
        print_json(error_to_dict("resource_list", err, {"busi_type": args.busi_type}), 1)


def command_capture(args, auth_context):
    try:
        request_payload = {"busiFlag": args.busi_type, "resourceTable": args.resource_table}
        x_de_token, runtime_info = resolve_capture_token(args, auth_context, "/de2api/dataVisualization/tree", request_payload)
        headers = build_token_headers(x_de_token)
        resource_tree = query_resource_tree(args.base_url, headers, args.busi_type, args.resource_table)
        resources = flatten_tree(extract_tree_nodes(resource_tree))

        if args.resource_id:
            target = next((item for item in resources if str(item.get("id")) == str(args.resource_id)), None)
            if not target:
                raise ValueError(f"资源树中未找到 resource_id={args.resource_id}")
            if not target.get("leaf"):
                raise ValueError(f"resource_id={args.resource_id} 对应的是目录节点，不能直接导出")
            resolved_query = target.get("name")
            candidates = [{
                "score": None,
                "id": target.get("id"),
                "name": target.get("name"),
                "leaf": target.get("leaf"),
                "type": target.get("type"),
            }]
        else:
            resolved, code = resolve_resource(resources, args.resource_name, args.alias_file, args.min_score)
            if code != 0:
                print_json({**resolved, **runtime_info}, code)
            target = resolved["resource"]
            resolved_query = resolved["resolved_query"]
            candidates = resolved["candidates"]

        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_name = re.sub(r"[^\w\u4e00-\u9fff-]+", "_", target["name"]).strip("_") or "capture"
        ext = guess_extension(args.result_format, "")
        output_path = (output_dir / f"{safe_name}_{target['id']}{ext}").resolve()
        preview_url = build_preview_url(args.base_url, target["id"], args.busi_type)
        browser_result = run_browser_capture(
            preview_url,
            x_de_token,
            args.pixel,
            args.ext_wait_time,
            args.result_format,
            output_path,
        )
    except Exception as err:
        extra = {
            "busi_type": args.busi_type,
        }
        if getattr(args, "resource_name", None):
            extra["resource_name"] = args.resource_name
        if getattr(args, "resource_id", None):
            extra["resource_id"] = args.resource_id
        print_json(error_to_dict("capture", err, extra), 1)

    print_json({
        "ok": True,
        "stage": "capture",
        "resource_id": target["id"],
        "resource_name": target["name"],
        "resolved_query": resolved_query,
        "busi_type": args.busi_type,
        "pixel": args.pixel,
        "ext_wait_time": args.ext_wait_time,
        "result_format": args.result_format,
        "preview_url": preview_url,
        "saved_file": str(output_path),
        "candidates": candidates,
        "capture_engine": "local_playwright",
        "capture_meta": browser_result,
        **runtime_info,
    }, 0)


def main():
    load_dotenv(ROOT_DIR / ".env")
    args = parse_args()
    auth_context = load_auth(args)

    if args.command == "list-orgs":
        command_list_orgs(args, auth_context)
    elif args.command == "switch-org":
        command_switch_org(args, auth_context)
    elif args.command == "list-resources":
        command_list_resources(args, auth_context)
    elif args.command == "capture":
        command_capture(args, auth_context)
    else:
        print_json({"ok": False, "stage": "args", "error": f"不支持的命令: {args.command}"}, 1)


if __name__ == "__main__":
    main()
