#!/usr/bin/env python3
"""
AK 认证与配置路径管理

职责：
1. OpenClaw 配置文件路径解析（候选目录收集、写入目录选择）
2. AK 读取（环境变量 + 配置文件 fallback）
3. API 请求签名构建
"""

import hashlib
import hmac
import base64
import time
import uuid
import logging
import json
import os
from pathlib import Path
from typing import Optional, Dict, Tuple
from urllib.parse import urlparse, parse_qs, quote
from _const import SKILL_VERSION, SKILL_ROOT, SCRIPT_DIR

logger = logging.getLogger(__name__)


# ── OpenClaw 配置文件路径 ────────────────────────────────────────
# 候选目录（按优先级）：
#   1. AGENT_WORK_ROOT 环境变量
#   2. Path.home()/workspace  （标准路径）
#   3. SKILL_ROOT/workspace   （skill 目录下，适用于 skill 被复制到 workspace 的场景）
#   4. 从 __file__ 绝对路径推断真实用户 home（适用于沙箱 HOME 被重写的场景）
#
# 写入：使用第一个可写路径（OPENCLAW_CONFIG_PATH）
# 读取：遍历所有候选路径（AK_CONFIG_PATH_CANDIDATES），返回第一个含有效 AK 的结果

def _collect_config_path_candidates() -> list:
    """收集所有候选配置目录，返回去重后的 Path 列表"""
    candidates: list[Path] = []

    # 1. 环境变量指定的目录（最高优先级）
    env_dir = os.environ.get("AGENT_WORK_ROOT")
    if env_dir:
        candidates.append(Path(env_dir) / "workspace")

    # 2. 标准 home 目录
    try:
        home_openclaw = Path.home() / "workspace"
        if home_openclaw not in candidates:
            candidates.append(home_openclaw)
    except Exception:
        pass

    # 3. Skill 根目录下的 .openclaw
    skill_openclaw = SKILL_ROOT / "workspace"
    if skill_openclaw not in candidates:
        candidates.append(skill_openclaw)

    # 4. 从 __file__ 绝对路径推断真实用户 home
    abs_parts = SCRIPT_DIR.parts
    if len(abs_parts) >= 3:
        real_home = Path(abs_parts[0]) / abs_parts[1] / abs_parts[2]
        real_openclaw = real_home / "workspace"
        if real_openclaw not in candidates:
            candidates.append(real_openclaw)

    return candidates


def _resolve_write_config_dir(candidates: list, sub_path: str = ".1688-AK", file_name: str = None) -> Path:
    """从候选列表中选出写入目录：优先已有 sub_path/file_name 的，其次第一个可写的"""
    if file_name:
        for d in candidates:
            if (d / sub_path / file_name).exists():
                return d / sub_path

    for d in candidates:
        target = d / sub_path
        try:
            target.mkdir(parents=True, exist_ok=True)
            return target
        except OSError:
            continue

    fallback = SKILL_ROOT / sub_path
    try:
        fallback.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    return fallback


# 所有候选配置文件路径（供读取时遍历）
WORKSPACE_DIR_CANDIDATES = _collect_config_path_candidates()
AK_CONFIG_PATH_CANDIDATES: list[Path] = [d / ".1688-AK" / ".ak_store.json" for d in WORKSPACE_DIR_CANDIDATES]

# 写入使用的配置文件路径（单一确定路径）
AK_CONFIG_PATH: Path = _resolve_write_config_dir(WORKSPACE_DIR_CANDIDATES, ".1688-AK", ".ak_store.json") / ".ak_store.json"

# ── OAuth 客户端配置 ──────────────────────────────────────────────────────────
OAUTH_CONFIG_DIR: Path = _resolve_write_config_dir(WORKSPACE_DIR_CANDIDATES, ".1688-oauth")
CLIENT_ID = os.environ.get("OAUTH_1688_CLIENT_ID", "3767346c-f079-4d16-8049-8ede627a480e")

# ── OAuth 服务端端点 ──
# 授权页面（用户在浏览器中完成登录授权）
AUTHORIZE_ENDPOINT = "https://air.1688.com/app/tai/oauth_page/index.html"
# 用 authorization_code 换取 Token 的网关端点
TOKEN_ENDPOINT = "https://skills-gateway.1688.com/api/get_token_by_auth_code/1.0.0"
# 用 Refresh Token 换取新 Token 的网关端点
REFRESH_TOKEN_ENDPOINT = "https://skills-gateway.1688.com/api/refresh_token/1.0.0"
# Revoke 端点（吊销 Access Token / Refresh Token，通过 tokenTypeHint 区分）
REVOKE_ENDPOINT = "https://skills-gateway.1688.com/api/revoke_token/1.0.0"
# Scope 列表查询端点
SCOPE_LIST_ENDPOINT = "https://skills-gateway.1688.com/api/query_all_scope/1.0.0"


# ── 回调服务器 ────────────────────────────────────────────────────────────────
CALLBACK_HOST = "localhost"
CALLBACK_BIND_ADDRESS = "127.0.0.1"
CALLBACK_PORT_START = 10000
CALLBACK_PORT_RETRIES = 10

# ── 超时 ──────────────────────────────────────────────────────────────────────
AUTHORIZATION_TIMEOUT = 300
HTTP_TIMEOUT = 30
TOKEN_REFRESH_MARGIN = 60
SCOPE_CACHE_TTL = 86400

# ── .env 文件 ─────────────────────────────────────────────────────────────────
ENV_FILE = OAUTH_CONFIG_DIR / ".env"

# ── Scope 缓存文件 ────────────────────────────────────────────────────────────
SCOPE_CACHE_FILE = OAUTH_CONFIG_DIR / ".scope_cache.json"

# ── .env / 安全存储中的 Token 变量名 ─────────────────────────────────────────
ENV_ACCESS_TOKEN = "OAUTH_1688_ACCESS_TOKEN"
ENV_REFRESH_TOKEN = "OAUTH_1688_REFRESH_TOKEN"
ENV_TOKEN_SCOPE = "OAUTH_1688_TOKEN_SCOPE"
ENV_TOKEN_EXPIRES_AT = "OAUTH_1688_TOKEN_EXPIRES_AT"
ENV_REFRESH_TOKEN_EXPIRES_AT = "OAUTH_1688_REFRESH_TOKEN_EXPIRES_AT"
ENV_CLIENT_ID = "OAUTH_1688_CLIENT_ID"
ENV_REDIRECT_URI = "OAUTH_1688_REDIRECT_URI"

# ── 授权模式 ──────────────────────────────────────────────────────────────────
AUTH_MODE_OAUTH = "oauth"
AUTH_MODE_AK = "AK"

# ── Keychain 服务名 ───────────────────────────────────────────────────────────
KEYCHAIN_SERVICE = "com.1688.oauth"

# ── 回调页面模板路径 ──────────────────────────────────────────────────────────
CALLBACK_TEMPLATE = Path(__file__).resolve().parent / "templates" / "callback.html"

# ── 数据存储目录（加密 Token 存储等）────────────────────────────────
DATA_DIR = OAUTH_CONFIG_DIR

def extract_ak_keys(raw_ak: str) -> tuple[Optional[str], Optional[str]]:
    """
    从原始 AK 字符串中提取 AccessKeyID 和 AccessKeySecret。
    AK 格式：base64url 编码后，前 32 位为 Secret，剩余为 ID。
    """
    if not raw_ak:
        return None, None

    try:
        padded = raw_ak + "=" * (-len(raw_ak) % 4)
        decoded = base64.urlsafe_b64decode(padded).decode("utf-8")
        secret = decoded[:32]
        ak_id = decoded[32:]
        if ak_id:
            return ak_id, secret
    except Exception:
        pass

    if len(raw_ak) > 32:
        return raw_ak[32:], raw_ak[:32]

    return None, None

def _get_ak_raw_from_config() -> Optional[str]:
    """从所有候选配置路径中读取 AK。
    文件格式：{"ak": "..."}，遍历 AK_CONFIG_PATH_CANDIDATES 直到找到有效值。"""
    for config_path in AK_CONFIG_PATH_CANDIDATES:
        if not config_path.exists():
            continue
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            ak = data.get("ak")
            if isinstance(ak, str) and ak:
                return ak
        except Exception:
            continue
    return None

def get_ak_from_env() -> Tuple[Optional[str], Optional[str]]:
    """读取 AK：优先环境变量（OpenClaw 注入），其次配置文件（Gateway 未重启时 fallback）"""
    raw_input = os.environ.get("ALI_1688_AK") or _get_ak_raw_from_config()
    if not raw_input:
        return None, None
    return extract_ak_keys(raw_input)

def _get_content_md5(body: str) -> str:
    """计算 body 的 MD5 并 Base64 编码"""
    if not body:
        return ""
    md5_obj = hashlib.md5(body.encode('utf-8'))
    return base64.b64encode(md5_obj.digest()).decode('utf-8')

def _get_canonicalized_resource(uri: str) -> str:
    parsed = urlparse(uri)
    path = parsed.path or "/"
    if not parsed.query:
        return path
    params = parse_qs(parsed.query, keep_blank_values=True)
    sorted_params = sorted(params.items())
    query_parts = []
    for key, values in sorted_params:
        for value in sorted(values):
            query_parts.append(f"{quote(key, safe='')}={quote(value, safe='')}")
    return f"{path}?{'&'.join(query_parts)}"

def build_signature(
    method: str,
    uri: str,
    body: str,
    content_type: str,
    ak_id: str,
    ak_secret: str
) -> Dict[str, str]:
    """
    构建带签名的请求头
    
    Args:
        method: HTTP 方法 (GET/POST)
        uri: 请求路径（包含查询参数）
        body: 请求体 JSON 字符串
        content_type: Content-Type
        ak_id: Access Key ID
        ak_secret: Access Key Secret
    
    Returns:
        完整的请求头字典
    """
    # A. 准备基础安全参数
    timestamp = str(int(time.time()))
    nonce = uuid.uuid4().hex[:8]
    content_md5 = _get_content_md5(body)
    
    # B. 构造自定义 Header
    csk_headers = {
        "x-csk-ak": ak_id,
        "x-csk-time": timestamp,
        "x-csk-nonce": nonce,
        "x-csk-content-md5": content_md5,
        "x-csk-version": SKILL_VERSION,
    }
    
    # C. 生成 CanonicalizedHeaders
    sorted_csk_keys = sorted(csk_headers.keys())
    canonicalized_headers = ""
    for key in sorted_csk_keys:
        canonicalized_headers += f"{key.lower()}:{csk_headers[key].strip()}\n"
    
    # D. 构造待签名字符串
    string_to_sign = (
        method.upper() + "\n" +
        content_md5 + "\n" +
        content_type + "\n" +
        timestamp + "\n" +
        canonicalized_headers +
        _get_canonicalized_resource(uri)
    )
    
    # E. 计算 HMAC-SHA256 签名
    signature = hmac.new(
        ak_secret.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha256
    ).digest()
    sign_base64 = base64.b64encode(signature).decode('utf-8')
    
    # F. 返回最终 Headers
    headers = {
        "Content-Type": content_type,
        "x-csk-sign": sign_base64,
        **csk_headers,
    }
    
    return headers

def get_auth_headers(method: str, uri: str, body: str = "") -> Optional[Dict[str, str]]:
    """
    获取认证头（便捷函数）
    
    Args:
        method: HTTP 方法
        uri: 请求 URI（如 /1688claw/skill/searchoffer）
        body: 请求体（JSON字符串）
    
    Returns:
        请求头字典，如果 AK 未配置则返回 None
    """
    ak_id, ak_secret = get_ak_from_env()
    
    if not ak_id or not ak_secret:
        logger.warning("AK 未配置，请先运行 configure 命令")
        return None
    
    return build_signature(
        method=method,
        uri=uri,
        body=body,
        content_type="application/json",
        ak_id=ak_id,
        ak_secret=ak_secret,
    )

# 别名：兼容 OAuth 模块中使用的 build_auth_headers 命名
build_auth_headers = get_auth_headers

# 测试入口
if __name__ == "__main__":
    # 从环境变量获取 AK 进行测试
    import os
    test_ak = os.environ.get("ALI_1688_AK")
    
    if not test_ak:
        print("❌ 请先设置环境变量 ALI_1688_AK")
        print("示例: export ALI_1688_AK=your_ak_here")
        exit(1)
    
    ak_id, ak_secret = extract_ak_keys(test_ak)
    if not ak_id or not ak_secret:
        print("❌ AK 格式不正确")
        exit(1)
    
    print(f"✅ AK ID: {ak_id}")
    print(f"✅ Secret: {ak_secret[:8]}...")
    
    # 测试签名生成
    headers = build_signature(
        method="POST",
        uri="/api/official_send_dingtalk_msg/1.0.0",
        body='{"title":"测试","userId":"123456","text":"测试消息"}',
        content_type="application/json",
        ak_id=ak_id,
        ak_secret=ak_secret,
    )
    
    print("\n✅ 签名生成成功！")
    print("请求头包含:")
    for k in headers.keys():
        print(f"  - {k}")