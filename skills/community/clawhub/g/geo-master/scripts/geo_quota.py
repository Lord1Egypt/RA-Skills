"""
GEO Monitor - 配额管理模块
免费版限制：每月1个品牌 + 3个平台
专业版：设置GEO_API_KEY环境变量即可解锁全部平台
"""
import json
import os
import time
from pathlib import Path

QUOTA_FILE = os.environ.get(
    "GEO_QUOTA_FILE",
    str(Path(__file__).parent.parent / ".geo_quota.json")
)

# 专业版API密钥（从环境变量读取）
# 设置此变量即自动识别为专业版用户
GEO_API_KEY = os.environ.get("GEO_API_KEY", "")

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
    if tier is None:
        # 有API_KEY视为专业版
        if GEO_API_KEY:
            tier = "pro"
        else:
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


def check_quota(keywords: list) -> tuple:
    """
    检查配额是否足够
    返回 (允许运行, 错误消息, 允许的平台列表)
    免费版：1个品牌 + 3个平台/月
    """
    quota = get_quota()
    tier = quota.get("tier", "free")

    # Pro/企业版不限制（有API_KEY也视为专业版）
    if tier in ["pro", "enterprise"] or GEO_API_KEY:
        effective_tier = tier if tier != "free" else "pro"
        enabled = get_enabled_platforms(effective_tier)
        return True, None, enabled

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
            f"访问 https://yk-global.com 了解详情。"
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
            f"访问 https://yk-global.com 了解详情。"
        ), None

    return True, None, enabled_platforms


def record_usage(keywords: list, platforms: list):
    """记录本次使用量"""
    quota = get_quota()

    # Pro/企业版不记录用量限制（有API_KEY也跳过）
    if quota.get("tier") in ["pro", "enterprise"] or GEO_API_KEY:
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


def show_quota_status():
    """显示配额状态"""
    quota = get_quota()
    tier = quota.get("tier", "free")

    if GEO_API_KEY:
        print(f"【专业版】已配置API密钥，无用量限制")
        return

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
    print("提示：专业版也可通过设置GEO_API_KEY环境变量启用，优先级更高")


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
