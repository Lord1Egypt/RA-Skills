"""
GEO Monitor - 配额管理模块
免费版限制：每月1个品牌 + 3个平台
专业版/企业版：通过 api.yk-global.com/v1/verify 验证 API Key 自动解锁
"""

import json
import os
import time
from pathlib import Path

# ─── yk global 验证接口 ──────────────────────────────────────────────────────
VERIFY_URL = "https://api.yk-global.com/v1/verify"
VERIFY_TIMEOUT = 10  # 秒


def verify_token(api_key: str) -> dict:
    """
    调用 yk global 验证接口验证 API Key。
    返回 dict：{"valid": bool, "tier": str, "error": str}
    网络错误或验证失败均返回 valid=False，降级到 FREE。
    """
    import urllib.request
    import urllib.error

    if not api_key:
        return {"valid": False, "tier": "FREE", "error": "未提供API Key"}

    try:
        req = urllib.request.Request(
            VERIFY_URL,
            method="POST",
            data=b"",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=VERIFY_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("success") and data.get("valid"):
                tier = _map_prefix_to_tier(data.get("prefix", ""))
                return {"valid": True, "tier": tier, "error": ""}
            else:
                return {"valid": False, "tier": "FREE", "error": data.get("error", "Key无效或已过期")}
    except urllib.error.HTTPError as e:
        return {"valid": False, "tier": "FREE", "error": f"HTTP {e.code}: Key无效或已过期"}
    except Exception as e:
        return {"valid": False, "tier": "FREE", "error": f"验证请求失败: {str(e)}"}


def _map_prefix_to_tier(prefix: str) -> str:
    """根据 API Key 前缀映射到 tier 级别。"""
    p = (prefix or "").upper()
    if "-FREE" in p or p == "FREE":
        return "FREE"
    if "-BSC" in p or "-BASIC" in p:
        return "BASIC"
    if "-STD" in p or "-STANDARD" in p:
        return "STANDARD"
    if "-PRO" in p:
        return "PRO"
    if "-ENT" in p or "-MAX" in p or "-ENTERPRISE" in p:
        return "ENTERPRISE"
    # 无法识别默认走 FREE
    return "FREE"


# ─── 本地配额文件 ─────────────────────────────────────────────────────────────
QUOTA_FILE = os.environ.get(
    "GEO_QUOTA_FILE",
    str(Path(__file__).parent.parent / ".geo_quota.json")
)

# 免费版限制
FREE_LIMIT_BRAND = 1
FREE_LIMIT_PLATFORM = 3


def get_quota():
    """获取当前配额，如果文件不存在或月份不同则初始化"""
    quota = {
        "brand_count": 0,
        "platforms_used": [],
        "month": get_current_month(),
        "total_runs": 0,
        "tier": "free"
    }

    if os.path.exists(QUOTA_FILE):
        try:
            with open(QUOTA_FILE, "r") as f:
                data = json.load(f)
            if data.get("month") != get_current_month():
                quota = {
                    "brand_count": 0,
                    "platforms_used": [],
                    "month": get_current_month(),
                    "total_runs": 0,
                    "tier": data.get("tier", "free")
                }
            else:
                quota = data
        except Exception:
            pass

    return quota


def save_quota(quota):
    """保存配额"""
    try:
        with open(QUOTA_FILE, "w") as f:
            json.dump(quota, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"配额保存失败: {e}")


def get_enabled_platforms(tier=None):
    """获取当前版本允许的平台列表"""
    # 有 API Key 优先用 yk global 验证
    geo_api_key = os.environ.get("GEO_API_KEY", "")
    if geo_api_key:
        result = verify_token(geo_api_key)
        if result["valid"]:
            tier = result["tier"]
        else:
            tier = "free"

    if tier is None:
        quota = get_quota()
        tier = quota.get("tier", "free")

    config_path = Path(__file__).parent.parent / "config.json"
    all_platforms = []
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            all_platforms = [k for k, v in config.get("platforms", {}).items() if v.get("enabled", False)]
        except Exception:
            pass

    # 免费版只允许3个平台
    if tier == "free":
        free_platforms = ["kimi", "xinhuo", "yiyan"]
        return [p for p in all_platforms if p in free_platforms]
    else:
        return all_platforms


def check_quota(keywords: list, api_key: str = None) -> tuple:
    """
    检查配额是否足够。
    api_key: 优先使用传入的 API Key（来自 --api-key 参数）
    返回 (允许运行, 错误消息, 允许的平台列表)
    免费版：1个品牌 + 3个平台/月
    """
    # 优先用传入的 api_key，否则读环境变量
    if not api_key:
        api_key = os.environ.get("GEO_API_KEY", "")

    # 通过 yk global 验证
    if api_key:
        result = verify_token(api_key)
        if result["valid"]:
            effective_tier = result["tier"]
            enabled = get_enabled_platforms(effective_tier)
            return True, None, enabled
        else:
            # 验证失败，降级 FREE，不阻断（容错）
            print(f"[警告] API Key 验证失败: {result['error']}，将以免费版运行")

    # 免费配额检查
    quota = get_quota()
    tier = quota.get("tier", "free")

    # 跨月重置配额（免费版）
    current_month = get_current_month()
    if quota.get("month") != current_month:
        quota["brand_count"] = 0
        quota["platforms_used"] = []
        quota["month"] = current_month
        quota["total_runs"] = 0
        save_quota(quota)

    # 获取本次要使用的平台
    enabled_platforms = get_enabled_platforms("free")

    # 计算已用品牌数
    brand_count = quota.get("brand_count", 0)
    new_brands = len(keywords)
    total_brands = brand_count + new_brands

    # 平台去重计算
    platforms_used = set(quota.get("platforms_used", []))
    platforms_this_run = set(enabled_platforms)
    new_platforms = platforms_this_run - platforms_used
    total_platforms = len(platforms_used) + len(new_platforms)

    # 检查品牌限制（免费版每月1个品牌）
    if total_brands > FREE_LIMIT_BRAND:
        return False, (
            f"【免费版限制】本月已检测{brand_count}个品牌，最多支持{FREE_LIMIT_BRAND}个品牌。\n"
            f"升级专业版可检测无限品牌，¥99/月。\n"
            f"如需购买收费版，请访问 https://yk-global.com"
        ), None

    # 检查平台限制（免费版每月3个平台）
    if total_platforms > FREE_LIMIT_PLATFORM:
        used_list = ", ".join(platforms_used) if platforms_used else "无"
        enabled_count = len(enabled_platforms)
        return False, (
            f"【免费版限制】本月已使用{len(platforms_used)}个平台（{used_list}），最多支持{FREE_LIMIT_PLATFORM}个AI平台。\n"
            f"本次运行将启用{enabled_count}个平台（{', '.join(enabled_platforms)}），\n"
            f"累计将超过{FREE_LIMIT_PLATFORM}个上限。\n\n"
            f"升级专业版可使用全部平台，¥99/月。\n"
            f"如需购买收费版，请访问 https://yk-global.com"
        ), None

    return True, None, enabled_platforms


def record_usage(keywords: list, platforms: list):
    """记录本次使用量"""
    quota = get_quota()

    # 专业版/企业版不记录用量限制
    if quota.get("tier") in ["pro", "enterprise"]:
        return

    # 累加品牌数
    quota["brand_count"] = quota.get("brand_count", 0) + len(keywords)

    # 合并平台（去重）
    platforms_used = set(quota.get("platforms_used", []))
    platforms_used.update(platforms)
    quota["platforms_used"] = list(platforms_used)

    # 次数+1
    quota["total_runs"] = quota.get("total_runs", 0) + 1

    save_quota(quota)


def get_current_month():
    """获取当前月份字符串"""
    return time.strftime("%Y-%m")


def show_quota_status(api_key: str = None):
    """显示配额状态"""
    if not api_key:
        api_key = os.environ.get("GEO_API_KEY", "")

    if api_key:
        result = verify_token(api_key)
        if result["valid"]:
            print(f"【{result['tier'].upper()}版】API Key 验证通过，无用量限制")
            return
        else:
            print(f"[警告] API Key 验证失败: {result['error']}，将以免费版运行")

    quota = get_quota()
    tier = quota.get("tier", "free")

    if tier in ["pro", "enterprise"]:
        print(f"【{tier.upper()}版】无用量限制")
        return

    brand_count = quota.get("brand_count", 0)
    platforms_used = quota.get("platforms_used", [])
    month = quota.get("month", get_current_month())

    print(f"【免费版】{month}配额: 品牌{brand_count}/{FREE_LIMIT_BRAND}, 平台{len(platforms_used)}/{FREE_LIMIT_PLATFORM}")
    if platforms_used:
        print(f"已用平台: {', '.join(platforms_used)}")


def upgrade_to_pro():
    """升级到专业版"""
    quota = get_quota()
    quota["tier"] = "pro"
    save_quota(quota)
    print("【升级成功】您现在是专业版用户，无品牌和平台限制")


def upgrade_to_enterprise():
    """升级到企业版"""
    quota = get_quota()
    quota["tier"] = "enterprise"
    save_quota(quota)
    print("【升级成功】您现在是企业版用户，无品牌和平台限制")


def downgrade_to_free():
    """降级到免费版"""
    quota = get_quota()
    quota["tier"] = "free"
    save_quota(quota)
    print("【降级完成】您现在是免费版用户")
