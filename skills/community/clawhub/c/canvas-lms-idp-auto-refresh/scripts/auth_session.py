from __future__ import annotations

import base64
import html
import logging
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

LOGGER = logging.getLogger("elearning_login")

DEFAULT_ENTRY_URL = "https://elearning.fudan.edu.cn/login/cas"
DEFAULT_ENTITY_ID = "https://elearning.fudan.edu.cn"
DEFAULT_IDP_BASE = "https://id.fudan.edu.cn"
DEFAULT_TIMEOUT = 20
DEFAULT_TOKEN_API = "https://elearning.fudan.edu.cn/api/v1/users/self/tokens"
DEFAULT_SETTINGS_REFERER = "https://elearning.fudan.edu.cn/profile/settings"


class FlowError(RuntimeError):
    """业务流程错误。"""


@dataclass
class AppConfig:
    username: str
    password: str
    entry_url: str = DEFAULT_ENTRY_URL
    entity_id: str = DEFAULT_ENTITY_ID
    idp_base_url: str = DEFAULT_IDP_BASE
    timeout_seconds: int = DEFAULT_TIMEOUT
    token_api_url: str = DEFAULT_TOKEN_API
    settings_referer: str = DEFAULT_SETTINGS_REFERER
    token_purpose: str = "OpenClaw Auto Refresh Token"


@dataclass
class IdpContext:
    lck: str
    auth_chain_code: str
    entity_id: str


@dataclass
class PublicKeyPayload:
    key: RSA.RsaKey
    source: str


@dataclass
class HandoffTarget:
    method: str
    url: str
    form_data: dict[str, str]


@dataclass
class LoginPreparationResult:
    entry_response: requests.Response
    lck: str
    auth_chain_code: str
    auth_methods_body: dict[str, Any]
    public_key_payload: PublicKeyPayload
    public_key_body: dict[str, Any]
    encrypted_password: str | None = None
    auth_body: dict[str, Any] | None = None
    login_token: str | None = None
    authn_engine_response: requests.Response | None = None


class ElearningAuthClient:
    """仅负责 IDP 登录与会话建立，便于复用。"""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0"
                ),
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
        )

    def fetch_entry(self) -> requests.Response:
        res = self.session.get(
            self.config.entry_url,
            timeout=self.config.timeout_seconds,
            allow_redirects=True,
        )
        res.raise_for_status()
        LOGGER.info("入口访问完成。final_url=%s", res.url)
        return res

    def resolve_lck(self, res: requests.Response) -> str:
        lck = extract_lck_from_url(res.url)
        if lck:
            return lck

        lck = extract_lck_from_text(res.text)
        if lck:
            return lck

        raise FlowError("未能从入口响应中解析到 lck。")

    def query_auth_methods(self, lck: str) -> tuple[str, dict[str, Any]]:
        url = f"{self.config.idp_base_url}/idp/authn/queryAuthMethods"
        payload = {
            "lck": lck,
            "entityId": self.config.entity_id,
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": self.config.idp_base_url,
            "Referer": f"{self.config.idp_base_url}/",
        }

        res = self.session.post(
            url,
            json=payload,
            headers=headers,
            timeout=self.config.timeout_seconds,
        )
        res.raise_for_status()

        body = res.json()
        auth_chain_code = pick_auth_chain_code(body)
        LOGGER.info("queryAuthMethods 成功。auth_chain_code=%s", mask(auth_chain_code))
        return auth_chain_code, body

    def get_js_public_key(self) -> tuple[PublicKeyPayload, dict[str, Any]]:
        url = f"{self.config.idp_base_url}/idp/authn/getJsPublicKey"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": self.config.idp_base_url,
            "Referer": f"{self.config.idp_base_url}/",
        }

        res = self.session.post(
            url,
            data="",
            headers=headers,
            timeout=self.config.timeout_seconds,
        )
        res.raise_for_status()

        body = res.json()
        key_payload = parse_public_key_payload(body)
        LOGGER.info("getJsPublicKey 成功。source=%s", key_payload.source)
        return key_payload, body

    def auth_execute(self, context: IdpContext, encrypted_password: str) -> dict[str, Any]:
        url = f"{self.config.idp_base_url}/idp/authn/authExecute"
        payload = {
            "authModuleCode": "userAndPwd",
            "authChainCode": context.auth_chain_code,
            "entityId": context.entity_id,
            "requestType": "chain_type",
            "lck": context.lck,
            "authPara": {
                "loginName": self.config.username,
                "password": encrypted_password,
                "verifyCode": "",
            },
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": self.config.idp_base_url,
            "Referer": f"{self.config.idp_base_url}/",
        }

        res = self.session.post(
            url,
            json=payload,
            headers=headers,
            timeout=self.config.timeout_seconds,
        )
        res.raise_for_status()

        body = res.json()
        code = body.get("code")
        if not is_success_code(code):
            raise FlowError(f"authExecute 返回非成功 code={code} message={body.get('message')}")

        LOGGER.info("authExecute 调用完成。")
        return body

    def submit_authn_engine(self, login_token: str) -> requests.Response:
        url = f"{self.config.idp_base_url}/idp/authCenter/authnEngine?locale=zh-CN"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8"
            ),
            "Origin": "null",
            "Referer": f"{self.config.idp_base_url}/",
        }

        res = self.session.post(
            url,
            data={"loginToken": login_token},
            headers=headers,
            allow_redirects=True,
            timeout=self.config.timeout_seconds,
        )
        LOGGER.info("authnEngine 提交完成。status=%s final_url=%s", res.status_code, res.url)

        handoff = parse_authn_engine_handoff(res.text)
        if handoff and "elearning.fudan.edu.cn" not in res.url:
            LOGGER.info("检测到浏览器跳转页，执行手动漫游。method=%s url=%s", handoff.method, handoff.url)
            if handoff.method == "POST":
                res = self.session.post(
                    handoff.url,
                    data=handoff.form_data,
                    allow_redirects=True,
                    timeout=self.config.timeout_seconds,
                    headers={"Referer": url},
                )
            else:
                res = self.session.get(
                    handoff.url,
                    params=handoff.form_data,
                    allow_redirects=True,
                    timeout=self.config.timeout_seconds,
                    headers={"Referer": url},
                )
            LOGGER.info("手动漫游完成。status=%s final_url=%s", res.status_code, res.url)

        return res

    def ensure_elearning_session_ready(self, res: requests.Response) -> None:
        cookie_names = {cookie.name for cookie in self.session.cookies}
        required = {"_normandy_session", "_csrf_token"}
        missing = required - cookie_names

        if missing:
            short = (res.text or "")[:400]
            hint = ""
            low = short.lower()
            if "captcha" in low or "verifycode" in low:
                hint = "疑似触发验证码/风控。"
            elif "login" in low or "error" in low:
                hint = "疑似账号密码错误、加密异常或 lck/authChainCode 过期。"
            raise FlowError(
                f"未拿到关键会话 Cookie: {sorted(missing)}。final_url={res.url}。{hint}"
            )

        LOGGER.info("会话就绪。已拿到 _normandy_session 与 _csrf_token")

    def extract_csrf(self) -> str:
        csrf = self.session.cookies.get("_csrf_token", domain="elearning.fudan.edu.cn")
        if not csrf:
            for cookie in self.session.cookies:
                if cookie.name == "_csrf_token":
                    csrf = cookie.value
                    break

        if not csrf:
            raise FlowError("会话中不存在 _csrf_token")

        return unquote(csrf)

    def login_and_prepare_session(self, *, dry_run: bool = False) -> LoginPreparationResult:
        """执行从入口到会话就绪的登录链路。dry_run=True 时只跑到公钥阶段。"""
        entry_res = self.fetch_entry()
        lck = self.resolve_lck(entry_res)
        auth_chain_code, auth_methods_body = self.query_auth_methods(lck)
        public_key_payload, public_key_body = self.get_js_public_key()

        result = LoginPreparationResult(
            entry_response=entry_res,
            lck=lck,
            auth_chain_code=auth_chain_code,
            auth_methods_body=auth_methods_body,
            public_key_payload=public_key_payload,
            public_key_body=public_key_body,
        )

        if dry_run:
            return result

        context = IdpContext(
            lck=lck,
            auth_chain_code=auth_chain_code,
            entity_id=self.config.entity_id,
        )
        encrypted_password = encrypt_password_rsa(self.config.password, public_key_payload.key)
        auth_body = self.auth_execute(context, encrypted_password)
        login_token = extract_login_token(auth_body)
        authn_engine_res = self.submit_authn_engine(login_token)
        self.ensure_elearning_session_ready(authn_engine_res)

        result.encrypted_password = encrypted_password
        result.auth_body = auth_body
        result.login_token = login_token
        result.authn_engine_response = authn_engine_res
        return result


def extract_lck_from_url(url: str) -> str:
    parsed = urlparse(url)

    qs = parse_qs(parsed.query)
    lck_values = qs.get("lck")
    if lck_values and lck_values[0]:
        return lck_values[0]

    fragment = parsed.fragment or ""
    if "?" in fragment:
        fragment_query = fragment.split("?", 1)[1]
        fragment_qs = parse_qs(fragment_query)
        frag_lck = fragment_qs.get("lck")
        if frag_lck and frag_lck[0]:
            return frag_lck[0]

    return ""


def extract_lck_from_text(text: str) -> str:
    patterns = [
        r"context_CAS_[0-9a-zA-Z]+",
        r'"lck"\s*[:=]\s*"(context_CAS_[0-9a-zA-Z]+)"',
        r"'lck'\s*[:=]\s*'?(context_CAS_[0-9a-zA-Z]+)'?",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if not match:
            continue
        if match.groups():
            return match.group(1)
        return match.group(0)
    return ""


def pick_auth_chain_code(body: dict[str, Any]) -> str:
    data = body.get("data")
    if not isinstance(data, list):
        raise FlowError("queryAuthMethods 响应缺少 data 列表")

    for item in data:
        if not isinstance(item, dict):
            continue
        module_code = str(item.get("moduleCode") or "")
        chain_name = str(item.get("chainName") or "")
        chain_code = str(item.get("authChainCode") or "")
        if module_code == "userAndPwd" and chain_code:
            return chain_code
        if "用户名密码" in chain_name and chain_code:
            return chain_code

    raise FlowError("queryAuthMethods 未找到 userAndPwd 对应 authChainCode")


def parse_public_key_payload(body: dict[str, Any]) -> PublicKeyPayload:
    direct_data = body.get("data")
    if isinstance(direct_data, str):
        key = try_parse_rsa_key(direct_data)
        if key:
            return PublicKeyPayload(key=key, source="data")

    candidates = collect_possible_public_key_values(body)

    for source, value in candidates:
        try:
            rsa_key = try_parse_rsa_key(value)
            if rsa_key:
                return PublicKeyPayload(key=rsa_key, source=source)
        except Exception:
            continue

    modulus, exponent = collect_modulus_exponent(body)
    if modulus and exponent:
        try:
            key = RSA.construct((int(modulus, 16), int(exponent, 16)))
            return PublicKeyPayload(key=key, source="modulus+exponent(hex)")
        except Exception as exc:  # noqa: BLE001
            raise FlowError(f"公钥解析失败（modulus/exponent）: {exc}") from exc

    raise FlowError("无法从 getJsPublicKey 响应中解析 RSA 公钥")


def is_success_code(code: Any) -> bool:
    if isinstance(code, int):
        return code == 200
    if isinstance(code, str):
        return code.strip() == "200"
    return False


def collect_possible_public_key_values(body: dict[str, Any]) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []

    def visit(prefix: str, value: Any) -> None:
        if isinstance(value, dict):
            for k, v in value.items():
                key_name = str(k)
                next_prefix = f"{prefix}.{key_name}" if prefix else key_name
                visit(next_prefix, v)
            return

        if isinstance(value, str):
            key_name = prefix.lower()
            if any(k in key_name for k in ("publickey", "pubkey", "key", "rsa")):
                trimmed = value.strip()
                if trimmed:
                    results.append((prefix, trimmed))

    visit("", body)
    return results


def collect_modulus_exponent(body: dict[str, Any]) -> tuple[str, str]:
    modulus = ""
    exponent = ""

    def visit(value: Any) -> None:
        nonlocal modulus, exponent
        if isinstance(value, dict):
            for k, v in value.items():
                lower = str(k).lower()
                if lower in {"modulus", "n"} and isinstance(v, str):
                    modulus = v.strip()
                elif lower in {"exponent", "e"} and isinstance(v, str):
                    exponent = v.strip()
                else:
                    visit(v)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(body)
    return modulus, exponent


def try_parse_rsa_key(raw: str) -> RSA.RsaKey | None:
    text = raw.strip()
    if not text:
        return None

    if "BEGIN PUBLIC KEY" in text:
        return RSA.import_key(text)

    try:
        decoded = base64.b64decode(text)
        try:
            return RSA.import_key(decoded)
        except ValueError:
            pass
    except Exception:
        pass

    try:
        return RSA.import_key(text.encode("utf-8"))
    except Exception:
        return None


def encrypt_password_rsa(password: str, pub_key: RSA.RsaKey) -> str:
    cipher = PKCS1_v1_5.new(pub_key)
    encrypted = cipher.encrypt(password.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


def extract_login_token(auth_execute_body: dict[str, Any]) -> str:
    direct_fields = ["loginToken", "token", "data", "result"]

    for field in direct_fields:
        value = auth_execute_body.get(field)
        token = find_jwt_token(value)
        if token:
            return token

    token = find_jwt_token(auth_execute_body)
    if token:
        return token

    raise FlowError("未从 authExecute 响应中提取到 loginToken（JWT）")


def parse_authn_engine_handoff(html_text: str) -> HandoffTarget | None:
    action_type_match = re.search(r'actionType\s*=\s*"(GET|POST)"', html_text, flags=re.IGNORECASE)
    location_match = re.search(r'locationValue\s*=\s*"([^"]+)"', html_text)

    action_type = "GET"
    if action_type_match:
        action_type = action_type_match.group(1).upper()

    if location_match:
        url = html.unescape(location_match.group(1))
        return HandoffTarget(method=action_type, url=url, form_data={})

    form_match = re.search(
        r'<form[^>]*method\s*=\s*"?(GET|POST)"?[^>]*action\s*=\s*"([^"]+)"[^>]*>(.*?)</form>',
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not form_match:
        return None

    method = form_match.group(1).upper()
    action = html.unescape(form_match.group(2))
    form_body = form_match.group(3)
    pairs = re.findall(
        r'<input[^>]*name\s*=\s*"([^"]+)"[^>]*value\s*=\s*"([^"]*)"[^>]*>',
        form_body,
        flags=re.IGNORECASE,
    )
    data = {k: html.unescape(v) for k, v in pairs}
    return HandoffTarget(method=method, url=action, form_data=data)


def find_jwt_token(value: Any) -> str:
    if isinstance(value, str):
        text = value.strip()
        if re.fullmatch(r"[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", text):
            return text
        try:
            payload = __import__("json").loads(text)
        except Exception:
            return ""
        return find_jwt_token(payload)

    if isinstance(value, dict):
        for _, v in value.items():
            token = find_jwt_token(v)
            if token:
                return token
        return ""

    if isinstance(value, list):
        for item in value:
            token = find_jwt_token(item)
            if token:
                return token

    return ""


def mask(value: str, keep: int = 4) -> str:
    if not value:
        return "<empty>"
    if len(value) <= keep * 2:
        return "*" * len(value)
    return f"{value[:keep]}***{value[-keep:]}"
