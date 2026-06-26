#!/usr/bin/env python3
"""
飞书记账系统搭建脚本（单表版）
一站式完成：创建多维表格、建表、建字段、加选项。
仅创建一张「明细表」同时记录支出和收入，通过「类型」字段区分。

用法：
    python3 setup_bitable.py --app-id cli_xxx --app-secret xxx
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error

FEISHU_HOST = "https://open.feishu.cn"


def get_tenant_token(app_id: str, app_secret: str) -> str:
    """获取 Tenant Access Token"""
    url = f"{FEISHU_HOST}/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise RuntimeError(f"获取 Tenant Token 失败: {result}")
    return result["tenant_access_token"]


def api_post(url: str, payload: dict, token: str) -> dict:
    """调用飞书 base/v3 POST 接口"""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise RuntimeError(f"API 调用失败: {json.dumps(result, ensure_ascii=False)}")
    return result["data"]


def create_bitable(token: str) -> str:
    """创建多维表格，返回 base_token"""
    url = f"{FEISHU_HOST}/open-apis/base/v3/bases"
    data = api_post(url, {"name": "个人记账本"}, token)
    base_token = data["base_token"]
    print(f"✅ 创建多维表格: {base_token}")
    print(f"🔗 链接: https://bytedance.feishu.cn/base/{base_token}")
    return base_token


def create_table(token: str, base_token: str, name: str) -> str:
    """创建数据表，返回 table_id"""
    url = f"{FEISHU_HOST}/open-apis/base/v3/bases/{base_token}/tables"
    data = api_post(url, {"name": name}, token)
    table_id = data["id"]
    print(f"✅ 创建数据表「{name}」: {table_id}")
    return table_id


def create_field(token: str, base_token: str, table_id: str,
                 field_name: str, field_type: str, options: list[dict] = None) -> str:
    """创建字段，返回 field_id"""
    url = f"{FEISHU_HOST}/open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields"
    payload = {"field_name": field_name, "type": field_type}
    if options:
        payload["options"] = options
    data = api_post(url, payload, token)
    field_id = data["id"]
    print(f"✅ 创建字段「{field_name}」({field_type}): {field_id}")
    return field_id


def update_field_options(token: str, base_token: str, table_id: str,
                         field_id: str, field_name: str, options: list[dict]) -> str:
    """更新字段选项（单选/多选）"""
    time.sleep(1)  # 等待字段创建缓存生效
    url = f"{FEISHU_HOST}/open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields/{field_id}"
    payload = {"field_name": field_name, "type": "select", "options": options}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise RuntimeError(f"更新选项失败: {json.dumps(result, ensure_ascii=False)}")
    print(f"✅ 更新「{field_name}」选项")
    return field_id


def main():
    parser = argparse.ArgumentParser(description="飞书记账系统搭建脚本（单表版）")
    parser.add_argument("--app-id", required=True, help="飞书应用 App ID")
    parser.add_argument("--app-secret", required=True, help="飞书应用 App Secret")
    args = parser.parse_args()

    print("🚀 开始搭建飞书记账系统（单表版）...")

    # Step 1: 获取 Tenant Token
    token = get_tenant_token(args.app_id, args.app_secret)
    print("✅ 获取 Tenant Token 成功")

    # Step 2: 创建多维表格
    base_token = create_bitable(token)

    # Step 3: 创建一张数据表（明细表），同时记录支出和收入
    table_id = create_table(token, base_token, "明细表")

    # Step 4: 创建字段
    # 文本 — 格式：{日期} {时间}{备注}
    create_field(token, base_token, table_id, "文本", "text")
    # 月份 — 格式：YYYY-MM
    create_field(token, base_token, table_id, "月份", "text")
    # 金额
    create_field(token, base_token, table_id, "金额", "number")
    # 分类（支出+收入所有选项）
    fld_category = create_field(token, base_token, table_id, "分类", "single_select")
    update_field_options(token, base_token, table_id, fld_category, "分类", [
        # 支出分类（13个）
        {"name": "餐饮"}, {"name": "购物"}, {"name": "交通"}, {"name": "娱乐"},
        {"name": "通讯"}, {"name": "生活"}, {"name": "医疗"}, {"name": "住房"},
        {"name": "教育"}, {"name": "服饰"}, {"name": "数码"}, {"name": "运动"},
        {"name": "宠物"}, {"name": "其它"},
        # 收入分类（5个）
        {"name": "工资"}, {"name": "奖金"}, {"name": "兼职"}, {"name": "投资"},
    ])
    # 类型（支出/收入）
    fld_type = create_field(token, base_token, table_id, "类型", "single_select")
    update_field_options(token, base_token, table_id, fld_type, "类型", [
        {"name": "支出"}, {"name": "收入"},
    ])

    print("\n🎉 搭建完成！请保存以下凭证：")
    print(f"\n📋 App ID: {args.app_id}")
    print(f"📋 App Secret: {args.app_secret}")
    print(f"📋 Base Token: {base_token}")
    print(f"📋 明细表 Table ID: {table_id}")
    print(f"\n📊 多维表格链接: https://bytedance.feishu.cn/base/{base_token}")

    # 输出 JSON 供 AI 解析
    print("\n---JSON_OUTPUT_START---")
    print(json.dumps({
        "app_id": args.app_id,
        "app_secret": args.app_secret,
        "base_token": base_token,
        "table_id": table_id,
    }, ensure_ascii=False))
    print("---JSON_OUTPUT_END---")


if __name__ == "__main__":
    main()
