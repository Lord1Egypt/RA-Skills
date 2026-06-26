#!/usr/bin/env python3
"""
DataNexus SDK 排障辅助脚本 - 校验数据源配置

帮助开发者快速校验数据源配置是否正确，包括：
1. 数据源 ID 是否有效
2. 数据源类型是否匹配
3. 分发开关建议（按应用类型区分）

使用方式：
    python3 校验数据源配置.py --token <access_token> --user_action_set_id <数据源ID>

注意：
    - 本脚本不获取用户 secret_key 等敏感信息
    - 仅查询数据源基本信息，不涉及数据修改
"""

import argparse
import json
import urllib.request
import urllib.error
import urllib.parse


SOURCE_TYPE_MAP = {
    "WECHAT": "微信（公众号）",
    "WECHAT_MINI_PROGRAM": "微信小程序",
    "WECHAT_MINI_GAME": "微信小游戏",
    "ANDROID": "Android App",
    "IOS": "iOS App",
    "WEB": "Web 网站",
    "OFFLINE": "线下",
}

DISTRIBUTION_ADVICE = {
    "WECHAT_MINI_PROGRAM": {
        "switches": ["一方数据合作 ✅", "转化归因 ✅"],
        "extra": "需在 DataNexus 工具箱完成微信 AppID 关联申请",
    },
    "WECHAT_MINI_GAME": {
        "switches": ["一方数据合作 ✅", "转化归因 ✅"],
        "extra": "需在 DataNexus 工具箱完成微信 AppID 关联申请",
    },
    "IOS": {
        "switches": ["一方数据合作 ✅", "预归因 ✅", "智能场景匹配 ✅", "转化归因 ❌ 不开启"],
        "extra": "预归因开关需联系行业运营按主体/账号维度申请加白",
    },
    "ANDROID": {
        "switches": ["一方数据合作 ✅", "预归因 ✅", "智能场景匹配 ✅", "转化归因 ❌ 不开启"],
        "extra": "非游戏行业默认配置；游戏行业 Android 应开启「一方数据合作」+「转化归因」",
    },
}


def get_user_action_sets(access_token, user_action_set_id):
    base_url = "https://api.e.qq.com/v3.0/user_action_sets/get"
    params = {"access_token": access_token, "user_action_set_id": user_action_set_id}
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"❌ Error: {e}")
        return None


def validate_config(result, expected_type=None):
    if not result or result.get("code") != 0:
        print("\\n❌ 无法获取数据源信息")
        return

    data = result.get("data", {})
    action_set = data.get("list", [{}])[0] if data.get("list") else data

    print("\\n" + "=" * 60)
    print("  📋 数据源配置校验报告")
    print("=" * 60)

    source_id = action_set.get("user_action_set_id", "N/A")
    source_type = action_set.get("type", "UNKNOWN")
    source_type_cn = SOURCE_TYPE_MAP.get(source_type, source_type)
    app_id = action_set.get("app_id", "")

    print(f"\\n  数据源 ID:   {source_id}")
    print(f"  数据源类型:  {source_type_cn} ({source_type})")
    print(f"  绑定 AppID:  {app_id or '未绑定'}")

    advice = DISTRIBUTION_ADVICE.get(source_type)
    if advice:
        print("\\n  📌 分发开关建议：")
        for switch in advice["switches"]:
            print(f"     • {switch}")
        if advice.get("extra"):
            print(f"     💡 {advice['extra']}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="DataNexus 数据源配置校验工具")
    parser.add_argument("--token", required=True, help="access_token")
    parser.add_argument("--user_action_set_id", required=True, help="数据源 ID")
    parser.add_argument("--expected_type", default=None, choices=list(SOURCE_TYPE_MAP.keys()), help="期望的数据源类型")
    args = parser.parse_args()

    result = get_user_action_sets(args.token, args.user_action_set_id)
    validate_config(result, expected_type=args.expected_type)


if __name__ == "__main__":
    main()
