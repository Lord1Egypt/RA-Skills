"""
License 验证模块 — 免费试用 + Gumroad License验证
"""
import os, sys, json, time
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None

INSTALL_FILE = Path.home() / ".clipmatrix_install"
GUMROAD_VERIFY = "https://api.gumroad.com/v2/sales/"
PRODUCT_PERMALINK = "uunfl"


def _get_install_days() -> int:
    if not INSTALL_FILE.exists():
        return 0
    try:
        installed_at = float(INSTALL_FILE.read_text().strip())
        return (datetime.now() - datetime.fromtimestamp(installed_at)).days
    except (ValueError, OSError):
        return 0


def _record_install():
    if not INSTALL_FILE.exists():
        INSTALL_FILE.parent.mkdir(parents=True, exist_ok=True)
        INSTALL_FILE.write_text(str(datetime.now().timestamp()))


def _get_license_key(config: dict) -> str:
    return config.get("license", {}).get("key", "").strip()


def check_license(config: dict, silent: bool = False) -> dict:
    license_config = config.get("license", {})
    license_key = _get_license_key(config)
    enable_trial = license_config.get("enable_trial", True)
    trial_days = license_config.get("trial_days", 7)

    # 有 License Key → Gumroad 在线验证
    if license_key:
        return _validate_gumroad(license_key, silent)

    # 试用模式
    if not enable_trial:
        return {"valid": False, "plan": "locked", "message": "🔒 License required."}

    _record_install()
    days = _get_install_days()

    if days <= trial_days:
        remaining = trial_days - days
        msg = f"🎉 Free trial: Day {days}/{trial_days}"
        if remaining <= 2:
            msg += f" — {remaining} days left!"
        return {"valid": True, "plan": "trial", "remaining_days": remaining, "message": msg}

    store_url = license_config.get("store_url", "https://zplaze.gumroad.com/l/uunfl")
    return {
        "valid": False, "plan": "trial_expired",
        "message": (
            f"⏰ Free trial expired.\n"
            f"   👉 {store_url}\n"
            f"   Got a key? Add to config.yaml → license.key"
        )
    }


def _validate_gumroad(license_key: str, silent: bool = False) -> dict:
    """验证 Gumroad 订单ID（用户在购买邮件中收到的 Order ID）"""
    if not requests:
        return {"valid": True, "plan": "pro", "message": "✅ License accepted (offline)"}

    try:
        # 用 Gumroad Sale API 验证订单存在且属于 ClipMatrix
        r = requests.get(f"{GUMROAD_VERIFY}{license_key}", timeout=10)

        if r.status_code == 200:
            data = r.json()
            sale = data.get("sale", {})
            # 验证订单属于本产品
            if sale.get("product_permalink") == PRODUCT_PERMALINK:
                return {
                    "valid": True, "plan": "pro",
                    "message": f"✅ License valid — {sale.get('email', 'Pro')}"
                }
            else:
                return {"valid": False, "plan": "invalid",
                        "message": "🔒 Order ID not found for ClipMatrix"}

        return {"valid": False, "plan": "invalid", "message": "🔒 Invalid license key"}

    except requests.RequestException:
        return {"valid": True, "plan": "pro", "message": "✅ License accepted (offline)"}


def require_license(config: dict):
    result = check_license(config)
    print(f"\n  {result['message']}")
    if not result["valid"]:
        print("\n❌ Cannot continue without valid license.\n")
        sys.exit(1)
    return result
