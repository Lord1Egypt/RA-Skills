#!/usr/bin/env python3
"""
清空记账多维表格数据（单表版 — 只清理明细表）。
测试用，清空飞书多维表格中指定表的所有记录。
支持表名匹配：--table-name 明细表

用法：
    python3 cleanup_bitable.py --app-id cli_xxx --app-secret xxx \\
        --base-token XhPpbh... --table-name "明细表"
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error

FEISHU_HOST = "https://open.feishu.cn"


def get_tenant_token(app_id: str, app_secret: str) -> str:
    url = f"{FEISHU_HOST}/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise RuntimeError(f"获取 Tenant Token 失败: {result}")
    return result["tenant_access_token"]


def list_tables(token: str, base_token: str) -> list[dict]:
    url = f"{FEISHU_HOST}/open-apis/base/v3/bases/{base_token}/tables"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise RuntimeError(f"获取表列表失败: {result}")
    return [{"id": t["id"], "name": t["name"]} for t in result["data"]["tables"]]


def list_records(token: str, base_token: str, table_id: str,
                 offset: int = 0) -> dict:
    url = (f"{FEISHU_HOST}/open-apis/base/v3/bases/{base_token}"
           f"/tables/{table_id}/records?page_size=100&offset={offset}")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise RuntimeError(f"获取记录失败: {result}")
    return result["data"]


def delete_record(token: str, base_token: str, table_id: str, record_id: str) -> bool:
    url = (f"{FEISHU_HOST}/open-apis/base/v3/bases/{base_token}"
           f"/tables/{table_id}/records/{record_id}")
    req = urllib.request.Request(url, method="DELETE",
                                 headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read()).get("code") == 0
    except urllib.error.HTTPError:
        return False


def main():
    parser = argparse.ArgumentParser(description="清空记账多维表格数据（单表版）")
    parser.add_argument("--app-id", required=True, help="飞书应用 App ID")
    parser.add_argument("--app-secret", required=True, help="飞书应用 App Secret")
    parser.add_argument("--base-token", required=True, help="多维表格 Base Token")
    parser.add_argument("--table-name", default="明细表", help="要清空的表名（默认：明细表）")
    args = parser.parse_args()

    print("🚀 开始清理记账数据...")
    token = get_tenant_token(args.app_id, args.app_secret)
    print("✅ 获取 Tenant Token 成功")

    tables = list_tables(token, args.base_token)
    target = None
    for t in tables:
        if t["name"] == args.table_name:
            target = t
            break
    if not target:
        print(f"❌ 未找到表「{args.table_name}」，现有表：{[t['name'] for t in tables]}")
        sys.exit(1)

    print(f"📋 目标表：{target['name']} ({target['id']})")

    total_deleted = 0
    batch = 0
    offset = 0
    while True:
        batch += 1
        data = list_records(token, args.base_token, target["id"], offset)
        records = data.get("data", [])
        record_ids = data.get("record_id_list", [])

        if not records:
            print("✅ 全部记录已清理完毕" if total_deleted > 0 else "ℹ️ 表中没有记录")
            break

        print(f"  第{batch}页 (offset={offset}): {len(records)} 条", end="")
        deleted = 0
        for rec_id in record_ids:
            time.sleep(0.1)  # 避免频控
            if delete_record(token, args.base_token, target["id"], rec_id):
                deleted += 1
            else:
                print(" ⚠️ 删除失败")
        total_deleted += deleted
        print(f" → 删了 {deleted} 条")
        offset += len(records)

    print(f"\n✅ 总计清理 {total_deleted} 条记录")


if __name__ == "__main__":
    main()
