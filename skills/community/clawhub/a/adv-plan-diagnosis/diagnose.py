#!/usr/bin/env python3
"""
广告计划诊断助手 - 双平台简化版
巨量引擎：调用 promotion_diagnosis 接口 (GET)
腾讯广告：日报表API + 规则引擎（直接使用配置的 access_token）
"""

import argparse
import json
import sys
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ======================= 规则引擎（腾讯广告使用） =======================
def rule_based_diagnosis(metrics, target_cost=30.0):
    cost = metrics.get("cost", 0)
    impressions = metrics.get("impressions", 0)
    clicks = metrics.get("clicks", 0)
    conversion_cost = metrics.get("conversion_cost")
    ctr = (clicks / impressions * 100) if impressions > 0 else 0

    if cost < 10 and impressions < 1000:
        return {
            "status": "不起量",
            "reason": f"消耗{cost}元（<10元），展现{impressions}次（<1000）",
            "suggestion": "1. 检查出价是否过低\n2. 放宽定向\n3. 确认素材审核",
            "urgency": "中"
        }
    if conversion_cost is not None and conversion_cost > target_cost * 1.2:
        return {
            "status": "成本高",
            "reason": f"转化成本{conversion_cost}元，超出目标{target_cost}元的20%",
            "suggestion": "1. 降低出价5%-10%\n2. 优化落地页",
            "urgency": "高"
        }
    if ctr > 2.0 and conversion_cost is not None and conversion_cost > target_cost * 0.8:
        return {
            "status": "素材疲劳",
            "reason": f"点击率{ctr}%尚可但转化成本偏高",
            "suggestion": "1. 准备新素材A/B测试\n2. 复制计划",
            "urgency": "中"
        }
    return {
        "status": "正常",
        "reason": "指标正常",
        "suggestion": "保持观察",
        "urgency": "低"
    }


# ======================= 巨量引擎 API =======================
def diagnose_ocean_engine(account_id, ad_ids):
    token = os.getenv('OCEAN_ENGINE_ACCESS_TOKEN')
    if not token:
        raise Exception("请在 .env 中配置 OCEAN_ENGINE_ACCESS_TOKEN")

    url = "https://api.oceanengine.com/open_api/v3.0/tools/promotion_diagnosis/suggestion/get/"
    headers = {"Access-Token": token}
    promotion_ids_str = json.dumps(ad_ids)
    scenes_str = json.dumps(["CLEAN", "POTENTIAL", "ZOMBIE"])
    params = {
        "advertiser_id": account_id,
        "promotion_ids": promotion_ids_str,
        "scenes": scenes_str
    }

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"巨量引擎诊断接口错误: {result.get('message')}")

    data = result.get("data", {})
    # 增加无建议时的友好提示
    suggestion_list = data.get("suggestion_list", [])
    for item in suggestion_list:
        pid = item.get("promotion_id")
        scene_list = item.get("scene_list", [])
        has_valid = False
        for scene_item in scene_list:
            suggestions = scene_item.get("suggestions", [])
            if suggestions and any(sug is not None for sug in suggestions):
                has_valid = True
                break
        if not has_valid:
            item["user_message"] = f"广告计划 {pid} 当前暂无官方优化建议。可能原因：数据不足或表现正常。建议保持观察。"
    return data


# ======================= 腾讯广告 API（直接使用配置的 token） =======================
def diagnose_tencent_ads(account_id, adgroup_id, target_cost, start_date, end_date):
    token = os.getenv('TENCENT_ACCESS_TOKEN')
    if not token:
        raise Exception("请在 .env 中配置 TENCENT_ACCESS_TOKEN")

    url = 'https://api.e.qq.com/v1.1/daily_reports/get'
    params = {
        'access_token': token,
        'account_id': account_id,
        'level': 'REPORT_LEVEL_ADGROUP',
        'date_range': json.dumps({'start_date': start_date, 'end_date': end_date}),
        'filtering': json.dumps([{'field': 'adgroup_id', 'operator': 'EQUALS', 'values': [str(adgroup_id)]}]),
        'fields': json.dumps(['adgroup_id', 'cost', 'view_count', 'valid_click_count', 'conversions_count']),
        'page': 1,
        'page_size': 10
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data.get('code') != 0:
        raise Exception(f"腾讯广告报表获取失败: {data.get('message')}")

    report_list = data.get('data', {}).get('list', [])
    if not report_list:
        metrics = {"cost": 0, "impressions": 0, "clicks": 0, "conversion_cost": None}
    else:
        r = report_list[0]
        cost = r.get('cost', 0) / 100
        conversions = r.get('conversions_count', 0)
        conversion_cost = cost / conversions if conversions > 0 else None
        metrics = {
            "cost": round(cost, 2),
            "impressions": r.get('view_count', 0),
            "clicks": r.get('valid_click_count', 0),
            "conversion_cost": round(conversion_cost, 2) if conversion_cost else None
        }

    diagnosis = rule_based_diagnosis(metrics, target_cost)
    diagnosis["query_period"] = f"{start_date} 至 {end_date}"
    diagnosis["platform"] = "tencent_ads"
    diagnosis["adgroup_id"] = adgroup_id
    return diagnosis


# ======================= 主函数 =======================
def main():
    parser = argparse.ArgumentParser(description="广告计划诊断助手（双平台）")
    parser.add_argument("--platform", required=True, choices=["ocean_engine", "tencent_ads"])
    parser.add_argument("--account_id", required=True, help="广告主ID / 账户ID")
    parser.add_argument("--adgroup_id", required=True, help="广告ID / 计划ID（多个用逗号分隔，仅巨量支持多个）")
    parser.add_argument("--target_cost", type=float, default=30.0, help="目标转化成本（仅腾讯广告使用）")
    parser.add_argument("--days", type=int, default=1, help="查询天数（仅腾讯广告使用）")
    args = parser.parse_args()

    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')

    try:
        if args.platform == "ocean_engine":
            ad_ids = [int(x.strip()) for x in args.adgroup_id.split(",")]
            result = diagnose_ocean_engine(int(args.account_id), ad_ids)
            output = {
                "platform": "ocean_engine",
                "account_id": args.account_id,
                "diagnosis": result
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))

        elif args.platform == "tencent_ads":
            result = diagnose_tencent_ads(
                int(args.account_id),
                int(args.adgroup_id),
                args.target_cost,
                start_date,
                end_date
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))

        else:
            raise ValueError(f"不支持的平台: {args.platform}")

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))


if __name__ == "__main__":
    main()