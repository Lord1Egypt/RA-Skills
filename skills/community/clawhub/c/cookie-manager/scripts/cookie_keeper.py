#!/usr/bin/env python3
"""闲鱼Cookie自动保活脚本

功能:
  1. HTTP轻量检查fishclaw-mcp Cookie文件有效性
  2. 有效Cookie的HTTP访问即为保活
  3. 失效/即将过期Cookie发送QQBot告警
  4. 同步auto_ops token_manager状态
  5. 4端Cookie同步检查与自动修复(fishclaw JSON/.env/global_config.yml/auto-reply API)

用法:
  python cookie_keeper.py --mode keep_alive
  python cookie_keeper.py --mode check
  python cookie_keeper.py --mode sync   # 仅同步4端
"""

import argparse

import json
import os
import sys

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("cookie-manager", source="skills/cookie-manager/scripts/cookie_keeper.py")
import time
import hashlib
import base64
from datetime import datetime, timezone, timedelta

import logging
logger = get_logger("system", source="skills/cookie-manager/scripts/cookie_keeper.py")

# 项目根目录: scripts/ -> cookie-manager/ -> skills/ -> JueJin/ (root)
_JUEJIN_HOME = Path(os.environ.get("JUEJIN_HOME", str(Path(__file__).resolve().parent.parent.parent.parent)))
_DOTENV_PATH = _JUEJIN_HOME / ".env"

# 幂等性保护: 文件锁防止Cron任务重复执行
_LOCK_FILE = _JUEJIN_HOME / "data" / "locks" / "cookie_keeper.lock"
_LOCK_TIMEOUT_SEC = 1800  # 锁过期时间30分钟

def _acquire_lock() -> bool:
    """幂等性保护: 防止Cron任务重复执行"""
    _LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    if _LOCK_FILE.exists():
        age = time.time() - _LOCK_FILE.stat().st_mtime
        if age < _LOCK_TIMEOUT_SEC:
            print(json.dumps({"success": False, "data": {}, "error": f"另一个cookie_keeper实例正在运行(锁文件年龄{age:.0f}秒)", "code": "LOCKED"}, ensure_ascii=False))
            return False
        else:
            logger.warning(f"[cookie_keeper] 锁文件过期(年龄{age:.0f}秒)，强制获取锁")
    _LOCK_FILE.write_text(str(os.getpid()))
    return True

def _release_lock() -> None:
    """释放文件锁"""
    _LOCK_FILE.unlink(missing_ok=True)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from mcps.shared.atomic_write import atomic_write_text
# 导入统一Cookie管理器 (P1-2 Cookie统一迁移)
from mcps.shared.cookie_manager import resolve_cookie_path

if _DOTENV_PATH.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_DOTENV_PATH, override=False)
    except ImportError:
        for _line in _DOTENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                _k, _v = _k.strip(), _v.strip().strip("\"'")
                if _k and _k not in os.environ:
                    os.environ[_k] = _v

try:
    import httpx
    _HTTPX_AVAILABLE = True
except ImportError:
    _HTTPX_AVAILABLE = False

_SYS_PATH = str(_JUEJIN_HOME)
if _SYS_PATH not in sys.path:
    sys.path.insert(0, _SYS_PATH)

_ACCOUNT_INTERVAL = 1020

# 安全要求: 必须使用cryptography.fernet进行加密，禁止降级到弱加密
try:
    from cryptography.fernet import Fernet as _Fernet
    _FERNET_AVAILABLE = True
except ImportError:
    _FERNET_AVAILABLE = False
    # 安全修复(VULN-3): 不再降级到弱加密，强制要求安装cryptography

def _get_encryption_key() -> str:
    """从环境变量获取加密密钥，不存在则自动生成并保存到.env"""
    key = os.environ.get("COOKIE_ENCRYPTION_KEY", "")
    if key:
        return key
    # 首次使用自动生成密钥(必须Fernet可用)
    if not _FERNET_AVAILABLE:
        print(json.dumps({"success": False, "error": "cryptography库未安装，Cookie加密不可用。请执行: pip install cryptography", "code": "FERNET_REQUIRED"}, ensure_ascii=False))
        sys.exit(1)
    key = _Fernet.generate_key().decode()
    _save_key_to_env(key)
    return key

def _save_key_to_env(key: str) -> None:
    """将加密密钥保存到.env文件"""
    try:
        env_path = _DOTENV_PATH
        if not env_path.exists():
            atomic_write_text(str(env_path), f"COOKIE_ENCRYPTION_KEY={key}\n")
            os.environ["COOKIE_ENCRYPTION_KEY"] = key
            return
        content = env_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        updated = False
        new_lines = []
        for line in lines:
            if line.strip().startswith("COOKIE_ENCRYPTION_KEY="):
                new_lines.append(f"COOKIE_ENCRYPTION_KEY={key}")
                updated = True
            else:
                new_lines.append(line)
        if not updated:
            new_lines.append(f"COOKIE_ENCRYPTION_KEY={key}")
        atomic_write_text(str(env_path), "\n".join(new_lines))
        os.environ["COOKIE_ENCRYPTION_KEY"] = key
    except Exception as e:
        logger.error(f"cookie keeper异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": f"保存加密密钥失败: {e}", "code": "ENCRYPT-KEY-SAVE-ERR"}))

def _encrypt_data(data: str) -> str:
    """加密数据，使用Fernet加密(VULN-3修复: 移除弱加密降级)"""
    if not data:
        return data
    key = _get_encryption_key()  # Fernet不可用时会exit(1)
    return _Fernet(key.encode()).encrypt(data.encode()).decode()

def _decrypt_data(encrypted: str) -> str:
    """解密数据，Fernet解密失败则尝试旧版简单解密(向后兼容)"""
    if not encrypted:
        return encrypted
    key = _get_encryption_key()
    # 优先Fernet解密
    try:
        return _Fernet(key.encode()).decrypt(encrypted.encode()).decode()
    except Exception as e:
        logger.error(f"cookie keeper异常: {e}", exc_info=True)
        logger.error(f"[cookie-manager] Fernet解密失败，尝试旧版解密: {e}")
    # 向后兼容: 尝试旧版简单解密(仅用于迁移旧数据)
    decrypted = _simple_decrypt(encrypted, key)
    if decrypted is not None:
        return decrypted
    # 都失败则返回原文（旧版明文数据）
    return encrypted

def _simple_decrypt(encrypted: str, key: str) -> str | None:
    """简单解密，失败返回None"""
    try:
        k = hashlib.sha256(key.encode()).digest()
        data = base64.b64decode(encrypted)
        result = bytearray()
        for i, b in enumerate(data):
            result.append(b ^ k[i % len(k)])
        return result.decode("utf-8")
    except Exception as e:
        logger.error(f"[cookie_keeper] 解密失败: {e}")
        return None

_COOKIE_AGE_WARN = 5
_COOKIE_AGE_CRITICAL = 25

def _get_fishclaw_cookie_path(tenant_id: str = "") -> Path:
    """获取闲鱼Cookie文件路径(支持多租户)

    使用统一Cookie管理器resolve_cookie_path解析路径。
    来源: P1-2 Cookie统一迁移
    """
    return resolve_cookie_path("xianyu", tenant_id=tenant_id)

def _get_cookie_targets(tenant_id: str = "") -> dict:
    """获取4端Cookie分发目标(支持多租户)

    来源: P1-2 Cookie统一迁移
    """
    return {
        "fishclaw_mcp": _get_fishclaw_cookie_path(tenant_id),
        "env_file": _JUEJIN_HOME / ".env",
        "global_config": _JUEJIN_HOME / "data" / "xianyu" / "global_config.yml",
        # auto-reply API通过HTTP检查，无文件路径
    }

def _load_cookie_from_file(tenant_id: str = "") -> str:
    """从fishclaw-mcp的JSON Cookie文件加载Cookie字符串（自动解密加密数据）

    使用统一Cookie管理器解析路径 (P1-2 Cookie统一迁移)
    """
    cookie_path = _get_fishclaw_cookie_path(tenant_id)
    if not cookie_path.exists():
        return ""

    try:
        raw = atomic_read_json(cookie_path)
        # 支持两种格式: 裸数组 或 {"cookies": [...]} 包装
        if isinstance(raw, list):
            cookies = raw
        elif isinstance(raw, dict) and "cookies" in raw:
            cookies = raw["cookies"]
        else:
            logger.warning(f"[cookie_keeper] Cookie文件格式不支持: {type(raw)}")
            return ""
        # 解密每个cookie的value字段
        for c in cookies:
            if "value" in c and c["value"]:
                c["value"] = _decrypt_data(c["value"])
        cookie_str = '; '.join([f'{c["name"]}={c["value"]}' for c in cookies if c.get("name") and c.get("value")])
        return cookie_str
    except Exception as e:
        logger.error(f"cookie keeper异常: {e}", exc_info=True)
        return ""

def _estimate_cookie_age(cookie: str) -> float:
    try:
        for part in cookie.split(";"):
            part = part.strip()
            if "_m_h5_tk" in part and "=" in part:
                val = part.split("=", 1)[1].strip()
                ts_ms = val.split("_")[0]
                if ts_ms.isdigit():
                    ts_sec = int(ts_ms) / 1000.0
                    age = (time.time() - ts_sec) / 86400.0
                    return max(0.0, age)
    except Exception as e:
        logger.error(f"cookie keeper异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "COOKIE-AGE-ERR"}))
    return -1.0

def _check_single_cookie(cookie: str, idx: int = 1) -> dict:
    age_days = _estimate_cookie_age(cookie)

    if not cookie:
        return {
            "account": f"account_{idx}",
            "valid": False,
            "age_days": age_days,
            "status": "empty",
            "error": "Cookie为空",
        }

    # P1-15修复: 支持新版Cookie格式(tfstk/xlly_s/cbc)
    # 旧版格式: cookie2=...; unb=...
    # 新版格式: tfstk=...; xlly_s=...; cbc=...
    has_old_format = "cookie2" in cookie
    has_new_format = "tfstk" in cookie and "xlly_s" in cookie

    if not has_old_format and not has_new_format:
        return {
            "account": f"account_{idx}",
            "valid": False,
            "age_days": age_days,
            "status": "invalid_format",
            "error": "Cookie格式无效,缺少cookie2或tfstk/xlly_s字段",
        }

    # 新版Cookie: 使用tfstk中的时间戳估算年龄
    if has_new_format:
        for part in cookie.split(";"):
            part = part.strip()
            if part.startswith("tfstk="):
                val = part.split("=", 1)[1].strip()
                # tfstk格式: abcdefghijklmnopqrstuvwxy... 不含时间戳，跳过
                break

    if not _HTTPX_AVAILABLE:
        return {
            "account": f"account_{idx}",
            "valid": None,
            "age_days": age_days,
            "status": "format_ok_only",
            "error": "httpx未安装,无法验证实际有效性",
        }

    try:
        resp = httpx.get(
            "https://goofish.com",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "Cookie": cookie,
            },
            follow_redirects=False,
            timeout=15.0,
        )
        
        if resp.status_code == 200:
            body = resp.text
            logged_out_markers = ["登录", "login", "sign-in", "passport"]
            is_logged_out = any(m in body.lower() for m in logged_out_markers) and "userinfo" not in body.lower()
            if is_logged_out:
                return {
                    "account": f"account_{idx}",
                    "valid": False,
                    "age_days": age_days,
                    "status": "expired",
                    "error": "Cookie已失效(服务端判定未登录)",
                }
            return {
                "account": f"account_{idx}",
                "valid": True,
                "age_days": age_days,
                "status": "valid",
                "error": None,
            }
        elif resp.status_code in (301, 302, 303, 307, 308):
            location = resp.headers.get("location", "")
            if "login" in location.lower() or "passport" in location.lower():
                return {
                    "account": f"account_{idx}",
                    "valid": False,
                    "age_days": age_days,
                    "status": "expired",
                    "error": "Cookie已失效(重定向到登录页)",
                }
            return {
                "account": f"account_{idx}",
                "valid": True,
                "age_days": age_days,
                "status": "valid",
                "error": None,
            }
        else:
            return {
                "account": f"account_{idx}",
                "valid": False,
                "age_days": age_days,
                "status": "unknown",
                "error": f"Cookie验证返回非预期状态码: {resp.status_code}",
            }
    except httpx.TimeoutException:
        return {
            "account": f"account_{idx}",
            "valid": None,
            "age_days": age_days,
            "status": "timeout",
            "error": "Cookie验证超时",
        }
    except Exception as e:
        logger.error(f"cookie keeper异常: {e}", exc_info=True)
        return {
            "account": f"account_{idx}",
            "valid": None,
            "age_days": age_days,
            "status": "error",
            "error": f"Cookie验证异常: {str(e)}",
        }

def _keep_alive_single_cookie(cookie: str, idx: int = 1) -> dict:
    # HTTP访问即为保活
    return _check_single_cookie(cookie, idx)

def _send_alert(message: str, level: str = "WARN"):
    try:
        from scripts.notification import send_alert
        return send_alert(message, level)
    except ImportError as e:
        logger.error(f"cookie keeper异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "COOKIE-ALERT-IMPORT-ERR"}))

    try:
        alert_dir = _JUEJIN_HOME / "data" / "auto_ops"
        alert_dir.mkdir(parents=True, exist_ok=True)
        alert_path = alert_dir / "alerts.json"
        alerts = []
        if alert_path.exists():
            try:
                alerts = json.loads(alert_path.read_text("utf-8"))
            except Exception as e:
                logger.error(f"cookie keeper异常: {e}", exc_info=True)
                logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "COOKIE-ALERT-READ-ERR"}))
        now = datetime.now(timezone(timedelta(hours=8))).isoformat()
        alerts.append({"timestamp": now, "level": level, "message": message})
        if len(alerts) > 100:
            alerts = alerts[-100:]
        atomic_write_text(str(alert_path), json.dumps(alerts, ensure_ascii=False, indent=2))
        return {"success": True, "method": "本地文件"}
    except Exception as e:
        logger.error(f"cookie keeper异常: {e}", exc_info=True)
        return {"success": False, "method": "none", "error": str(e)}

def _sync_token_manager(results: list) -> bool:
    try:
        from mcps.shared.auto_ops import token_manager
        any_valid = any(r.get("valid") for r in results)
        token_manager.update(
            "xianyu_cookie",
            is_valid=any_valid,
            expires_in=int(os.environ.get("COOKIE_TTL_HOURS", "168")) * 3600 if any_valid else 0,
            error="" if any_valid else "Cookie检查发现全部失效",
        )
        return True
    except Exception as e:
        logger.error(f"[cookie_keeper] token_manager同步失败: {e}")
        return False

def _check_4port_sync(cookie_str: str, tenant_id: str = "") -> dict:
    """检查Cookie 4端同步状态(fishclaw JSON/.env/global_config.yml/auto-reply API)

    以fishclaw-mcp JSON文件为权威源，检查其他3端是否与之一致。
    返回每端的同步状态和整体同步结果。
    来源: P1-2 Cookie统一迁移(支持多租户)
    """
    sync_status = {}
    _cookie_targets = _get_cookie_targets(tenant_id)
    # 提取fishclaw JSON中的unb字段作为一致性标识
    source_unb = ""
    for part in cookie_str.split(";"):
        part = part.strip()
        if part.startswith("unb="):
            source_unb = part.split("=", 1)[1].strip()
            break

    # 1. 检查.env文件中的XIANYU_COOKIE_1（支持加密数据解密）
    env_path = _cookie_targets["env_file"]
    env_sync = {"exists": False, "has_cookie": False, "unb_match": False, "stale": False}
    if env_path.exists():
        env_sync["exists"] = True
        try:
            env_content = env_path.read_text(encoding="utf-8")
            for line in env_content.splitlines():
                stripped = line.strip()
                if stripped.startswith("XIANYU_COOKIE_1="):
                    env_cookie_raw = stripped.split("=", 1)[1].strip()
                    # 尝试解密（向后兼容明文数据）
                    env_cookie = _decrypt_data(env_cookie_raw) if env_cookie_raw else ""
                    if env_cookie and "cookie2" in env_cookie:
                        env_sync["has_cookie"] = True
                        env_unb = ""
                        for part in env_cookie.split(";"):
                            part = part.strip()
                            if part.startswith("unb="):
                                env_unb = part.split("=", 1)[1].strip()
                                break
                        env_sync["unb_match"] = (source_unb == env_unb) if source_unb else True
                        # 检查.env中Cookie获取时间
                        for line2 in env_content.splitlines():
                            if line2.strip().startswith("XIANYU_COOKIE_1_OBTAINED_AT="):
                                obtained = line2.strip().split("=", 1)[1].strip()
                                try:
                                    obtained_date = datetime.strptime(obtained, "%Y-%m-%d")
                                    age = (datetime.now() - obtained_date).days
                                    env_sync["stale"] = age > _COOKIE_AGE_WARN
                                    env_sync["age_days"] = age
                                except ValueError as e:
                                    logger.error(f"cookie keeper异常: {e}", exc_info=True)
                                    logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "COOKIE-DATE-ERR"}))
                    break
        except Exception as e:
            logger.error(f"cookie keeper异常: {e}", exc_info=True)
            env_sync["error"] = str(e)
    sync_status["env_file"] = env_sync

    # 2. 检查global_config.yml中的COOKIES.value（支持加密数据解密）
    yml_path = _cookie_targets["global_config"]
    yml_sync = {"exists": False, "has_cookie": False, "unb_match": False, "stale": False}
    if yml_path.exists():
        yml_sync["exists"] = True
        try:
            import yaml
            with open(yml_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            if config and isinstance(config, dict):
                cookies_val_raw = config.get("COOKIES", {}).get("value", "")
                # 尝试解密（向后兼容明文数据）
                cookies_val = _decrypt_data(str(cookies_val_raw)) if cookies_val_raw else ""
                if cookies_val and "cookie2" in cookies_val:
                    yml_sync["has_cookie"] = True
                    yml_unb = ""
                    for part in str(cookies_val).split(";"):
                        part = part.strip()
                        if part.startswith("unb="):
                            yml_unb = part.split("=", 1)[1].strip()
                            break
                    yml_sync["unb_match"] = (source_unb == yml_unb) if source_unb else True
                # 检查最后更新时间
                last_update = config.get("COOKIES", {}).get("last_update_time", "")
                if last_update:
                    try:
                        update_date = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
                        age = (datetime.now() - update_date).days
                        yml_sync["stale"] = age > _COOKIE_AGE_WARN
                        yml_sync["age_days"] = age
                    except ValueError as e:
                        logger.error(f"cookie keeper异常: {e}", exc_info=True)
                        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "COOKIE-DATE-ERR"}))
        except ImportError:
            yml_sync["error"] = "yaml模块未安装"
        except Exception as e:
            logger.error(f"cookie keeper异常: {e}", exc_info=True)
            yml_sync["error"] = str(e)
    sync_status["global_config"] = yml_sync

    # 3. 检查xianyu-auto-reply API
    api_sync = {"reachable": False, "has_cookie": False, "unb_match": False}
    auto_reply_url = os.environ.get("XIANYU_AUTO_REPLY_URL", "http://localhost:8290")
    if _HTTPX_AVAILABLE:
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(f"{auto_reply_url}/health")
                if resp.status_code == 200:
                    api_sync["reachable"] = True
                    # 尝试获取Cookie列表(需认证，简化检查)
                    api_sync["has_cookie"] = True  # 服务可达即认为可能已配置
        except Exception as e:
            logger.error(f"cookie keeper异常: {e}", exc_info=True)
            logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "COOKIE-API-ERR"}))
    sync_status["web_api"] = api_sync

    # 汇总同步状态
    all_in_sync = (
        env_sync.get("has_cookie") and env_sync.get("unb_match", True)
        and yml_sync.get("has_cookie") and yml_sync.get("unb_match", True)
        and api_sync.get("reachable", False)
    )
    needs_sync = (
        not env_sync.get("has_cookie") or not env_sync.get("unb_match", True)
        or not yml_sync.get("has_cookie") or not yml_sync.get("unb_match", True)
    )
    sync_status["_summary"] = {
        "all_in_sync": all_in_sync,
        "needs_sync": needs_sync,
        "source_unb": source_unb,
    }
    return sync_status

def _sync_to_3ports(cookie_str: str, cookie_dict: dict, tenant_id: str = "") -> dict:
    """将fishclaw-mcp的Cookie同步到其他3端(.env/global_config.yml/auto-reply API)

    仅在Cookie有效且4端不同步时调用。
    返回每端的同步结果。
    来源: P1-2 Cookie统一迁移(支持多租户)
    """
    results = {}
    _cookie_targets = _get_cookie_targets(tenant_id)

    # 1. 同步到.env（加密存储）
    env_path = _cookie_targets["env_file"]
    env_result = {"status": "skipped"}
    if env_path.exists() and cookie_str:
        try:
            encrypted_cookie = _encrypt_data(cookie_str)
            content = env_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            updated = False
            new_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("XIANYU_COOKIE_1="):
                    new_lines.append(f'XIANYU_COOKIE_1={encrypted_cookie}')
                    updated = True
                elif stripped.startswith("XIANYU_COOKIE_1_OBTAINED_AT="):
                    new_lines.append(f'XIANYU_COOKIE_1_OBTAINED_AT={datetime.now().strftime("%Y-%m-%d")}')
                else:
                    new_lines.append(line)
            if not updated:
                new_lines.append(f'\nXIANYU_COOKIE_1={encrypted_cookie}')
                new_lines.append(f'\nXIANYU_COOKIE_1_OBTAINED_AT={datetime.now().strftime("%Y-%m-%d")}')
            atomic_write_text(str(env_path), "\n".join(new_lines))
            env_result = {"status": "ok", "encrypted": True}
        except Exception as e:
            logger.error(f"cookie keeper异常: {e}", exc_info=True)
            env_result = {"status": "error", "message": str(e)}
    results["env_file"] = env_result

    # 2. 同步到global_config.yml（明文存储，P0-6修复）
    # xianyu-auto-reply容器的config.py直接读取COOKIES.value作为明文cookie字符串
    # 不支持encrypted标记和Fernet解密。写入加密cookie会导致容器启动时
    # "Cookie中缺少必需的'unb'字段"错误（加密串被当作cookie key=value解析）
    yml_path = _cookie_targets["global_config"]
    yml_result = {"status": "skipped"}
    if yml_path.exists() and cookie_str:
        try:
            import yaml
            with open(yml_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            config.setdefault("COOKIES", {})
            config["COOKIES"]["value"] = cookie_str
            config["COOKIES"]["last_update_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            config["COOKIES"]["encrypted"] = False
            atomic_write_text(str(yml_path), yaml.dump(config, allow_unicode=True, default_flow_style=False))
            yml_result = {"status": "ok", "encrypted": False}
        except ImportError:
            yml_result = {"status": "error", "message": "yaml模块未安装"}
        except Exception as e:
            logger.error(f"cookie keeper异常: {e}", exc_info=True)
            yml_result = {"status": "error", "message": str(e)}
    results["global_config"] = yml_result

    # 3. 同步到xianyu-auto-reply API
    api_result = {"status": "skipped"}
    auto_reply_url = os.environ.get("XIANYU_AUTO_REPLY_URL", "http://localhost:8290")
    if _HTTPX_AVAILABLE and cookie_str:
        try:
            with httpx.Client(timeout=10.0) as client:
                # 健康检查
                health = client.get(f"{auto_reply_url}/health")
                if health.status_code == 200:
                    # 登录获取token
                    admin_password = os.environ.get("XIANYU_ADMIN_PASSWORD", "")
                    if not admin_password:
                        return {"success": False, "error": "XIANYU_ADMIN_PASSWORD环境变量未设置", "code": "CONFIG_MISSING"}
                    login_resp = client.post(
                        f"{auto_reply_url}/login",
                        json={"username": "admin", "password": admin_password},
                    )
                    token_data = login_resp.json()
                    token = token_data.get("token") or token_data.get("access_token", "")
                    if token:
                        headers = {"Authorization": f"Bearer {token}"}
                        # 同步到default id(auto-reply默认使用default Cookie)
                        # 同时同步到unb对应的id(如14670459)
                        sync_ids = ["default"]
                        unb_val = cookie_dict.get("unb", "")
                        if unb_val and unb_val not in sync_ids:
                            sync_ids.append(unb_val)
                        for cookie_id in sync_ids:
                            add_resp = client.post(
                                f"{auto_reply_url}/cookies",
                                json={"id": cookie_id, "value": cookie_str},
                                headers=headers,
                            )
                            if add_resp.status_code in (200, 201):
                                api_result = {"status": "ok"}
                            else:
                                api_result = {"status": "warning", "message": f"API返回 {add_resp.status_code} for id={cookie_id}"}
                    else:
                        api_result = {"status": "warning", "message": "无法获取API token"}
                else:
                    api_result = {"status": "warning", "message": "服务不可达"}
        except httpx.ConnectError:
            api_result = {"status": "warning", "message": "服务未启动"}
        except Exception as e:
            logger.error(f"cookie keeper异常: {e}", exc_info=True)
            api_result = {"status": "error", "message": str(e)}
    results["web_api"] = api_result

    return results

def _compute_next_check() -> str:
    now = datetime.now(timezone(timedelta(hours=8)))
    # P1-14修复: 保活频率从3天改为2天,避免连续2次Cron失败后接近7天WARNING阈值
    # 2天保活+5天WARNING阈值=2.5次保活窗口,即使1次失败仍有1.5次保活余量
    next_time = now + timedelta(days=2)
    return next_time.strftime("%Y-%m-%dT%H:%M:%S")

def main():
    # 幂等性保护: 防止Cron任务重复执行
    """main"""
    if not _acquire_lock():
        sys.exit(0)
    try:
        _main_inner()
    finally:
        _release_lock()

def _main_inner():
    parser = argparse.ArgumentParser(description="闲鱼Cookie自动保活")
    parser.add_argument("--mode", choices=["keep_alive", "check", "force_refresh", "sync"], default="keep_alive",
                        help="运行模式: keep_alive=检查+保活+同步, check=仅检查, force_refresh=强制刷新token_manager, sync=仅4端同步")
    parser.add_argument("--tenant_id", default="", help="租户ID(支持多租户) (P1-2 Cookie统一迁移)")
    args = parser.parse_args()
    tenant_id = args.tenant_id

    # 加载统一管理的Cookie
    cookie = _load_cookie_from_file(tenant_id)

    if not cookie:
        error_msg = "Cookie文件不存在或无法读取"
        _fishclaw_path = _get_fishclaw_cookie_path(tenant_id)
        if not _fishclaw_path.exists():
            error_msg = f"Cookie文件不存在: {_fishclaw_path}"

        print(json.dumps({
            "success": False,
            "data": {"total": 0, "valid": 0, "invalid": 0, "results": [], "alerts_sent": 0, "token_manager_synced": False, "next_check": "", "sync_status": {}},
            "error": error_msg,
            "code": "NO_COOKIE",
        }))
        sys.exit(1)

    # 解析cookie_dict用于同步
    cookie_dict = {}
    for item in cookie.split(";"):
        item = item.strip()
        if "=" in item:
            k, v = item.split("=", 1)
            cookie_dict[k.strip()] = v.strip()

    # sync模式：仅执行4端同步
    if args.mode == "sync":
        sync_result = _check_4port_sync(cookie, tenant_id)
        if sync_result["_summary"]["needs_sync"]:
            sync_action = _sync_to_3ports(cookie, cookie_dict, tenant_id)
            output = {
                "success": True,
                "data": {
                    "sync_check": sync_result,
                    "sync_action": sync_action,
                    "was_out_of_sync": True,
                },
                "error": None,
                "code": "COOKIE_SYNC_OK",
            }
        else:
            output = {
                "success": True,
                "data": {
                    "sync_check": sync_result,
                    "sync_action": {},
                    "was_out_of_sync": False,
                },
                "error": None,
                "code": "COOKIE_ALREADY_SYNCED",
            }
        print(json.dumps(output, ensure_ascii=False))
        return

    # 统一视为 account_1 进行监控和报告
    idx = 1
    result = _check_single_cookie(cookie, idx)
    results = [result]

    # P1-14修复: 连续失败检测 - 读取上次保活结果,如果上次失败则提高告警优先级
    last_result_path = _JUEJIN_HOME / "data" / "cookie_keeper_last_result.json"
    last_result = {}
    if last_result_path.exists():
        try:
            last_result = json.loads(last_result_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            last_result = {}
    consecutive_failures = last_result.get("consecutive_failures", 0)
    if result.get("valid") is False:
        consecutive_failures += 1
    else:
        consecutive_failures = 0
    # 保存本次结果
    try:
        last_result_path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_text(str(last_result_path), json.dumps({
            "last_check": datetime.now(timezone(timedelta(hours=8))).isoformat(),
            "last_valid": result.get("valid"),
            "consecutive_failures": consecutive_failures,
        }, ensure_ascii=False))
    except Exception as e:
        logger.error(f"cookie keeper异常: {e}", exc_info=True)
        logger.warning(f"[cookie-manager] 保存上次检查结果失败: {e}")
    alerts_sent = 0  # 初始化告警计数，防止UnboundLocalError
    if args.mode == "keep_alive":
        # 连续失败≥2次时提高告警级别为CRITICAL
        if result["valid"] is False:
            severity = "CRITICAL" if consecutive_failures >= 2 else "CRITICAL"
            msg = f"🔴 闲鱼Cookie失效: 账号{idx} Cookie已失效,请发送'登录闲鱼'重新扫码"
            if consecutive_failures >= 2:
                msg += f" (连续{consecutive_failures}次失败,需立即处理!)"
            _send_alert(msg, severity)
            alerts_sent += 1
        elif result["valid"] is True and result.get("age_days", 0) >= _COOKIE_AGE_CRITICAL:
            msg = f"🔴 闲鱼Cookie严重预警: 账号{idx} Cookie已{result['age_days']:.0f}天,需立即续期"
            _send_alert(msg, "CRITICAL")
            alerts_sent += 1
        elif result["valid"] is True and result.get("age_days", 0) >= _COOKIE_AGE_WARN:
            msg = f"⚠️ 闲鱼Cookie预警: 账号{idx} Cookie已{result.get('age_days', 0):.0f}天,接近过期风险(5天安全线)"
            _send_alert(msg, "WARN")
            alerts_sent += 1

    token_synced = _sync_token_manager(results) if args.mode in ("keep_alive", "force_refresh") else False

    # 4端同步检查(Cookie有效时)
    sync_status = {}
    sync_action = {}
    if args.mode == "keep_alive" and result["valid"] is True:
        sync_status = _check_4port_sync(cookie, tenant_id)
        if sync_status.get("_summary", {}).get("needs_sync", False):
            sync_action = _sync_to_3ports(cookie, cookie_dict, tenant_id)
            if sync_action:
                msg = f"ℹ️ Cookie 4端同步: 检测到不同步,已自动修复({', '.join(k for k,v in sync_action.items() if v.get('status')=='ok')})"
                _send_alert(msg, "INFO")

    valid_count = sum(1 for r in results if r.get("valid") is True)
    invalid_count = sum(1 for r in results if r.get("valid") is False)

    output = {
        "success": True,
        "data": {
            "total": len(results),
            "valid": valid_count,
            "invalid": invalid_count,
            "results": results,
            "alerts_sent": alerts_sent,
            "token_manager_synced": token_synced,
            "next_check": _compute_next_check() if args.mode == "keep_alive" else "",
            "sync_status": sync_status,
            "sync_action": sync_action,
            "consecutive_failures": consecutive_failures,
        },
        "error": None,
        "code": "COOKIE_KEEPER_OK",
    }

    print(json.dumps(output, ensure_ascii=False))

    if invalid_count > 0 and args.mode == "keep_alive":
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        logger.error(f"cookie keeper异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "VALUE_ERROR"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        logger.error(f"cookie keeper异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "INTERNAL_ERROR"}, ensure_ascii=False))
        sys.exit(2)
