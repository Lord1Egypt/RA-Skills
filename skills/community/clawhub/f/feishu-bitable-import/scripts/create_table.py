#!/usr/bin/env python3
"""
从 CSV/Excel 自动创建飞书多维表格并导入数据
"""

import argparse
import pandas as pd
import os
from dotenv import load_dotenv
from sync import FeishuBitableSync

load_dotenv()

APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")


def create_bitable_table(
    sync: FeishuBitableSync,
    app_token: str,
    table_name: str,
    df: pd.DataFrame
) -> str:
    """创建新表格"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
    fields = []
    
    for col in df.columns:
        type_id = FeishuBitableSync.infer_field_type(df[col].tolist())
        fields.append({
            "field_name": col,
            "type": type_id
        })
    
    data = {
        "name": table_name,
        "fields": fields
    }
    
    resp = sync.request("POST", url, json=data)
    table_id = resp["data"]["table_id"]
    print(f"✅ 创建表格成功: {table_name} (table_id: {table_id})")
    return table_id


def main():
    parser = argparse.ArgumentParser(description='从 CSV 创建飞书多维表格并导入数据')
    parser.add_argument('--input', required=True, help='输入文件: .csv .xlsx .json')
    parser.add_argument('--app-token', required=True, help='飞书 app_token (Base ID)')
    parser.add_argument('--folder-token', help='文件夹 token (可选，新建 Base 需要)')
    parser.add_argument('--table-name', required=True, help='新表格名称')
    parser.add_argument('--sheet-name', help='Excel sheet 名称(可选)')
    args = parser.parse_args()
    
    # 读取数据
    input_path = args.input
    if input_path.endswith('.csv'):
        df = pd.read_csv(input_path, dtype=str)
    elif input_path.endswith('.xlsx') or input_path.endswith('.xls'):
        if args.sheet_name:
            df = pd.read_excel(input_path, sheet_name=args.sheet_name, dtype=str)
        else:
            df = pd.read_excel(input_path, dtype=str)
    elif input_path.endswith('.json'):
        df = pd.read_json(input_path)
    else:
        raise Exception("不支持的文件格式，请使用 .csv .xlsx .json")
    
    print(f"读取数据完成: {len(df)} 行 × {len(df.columns)} 列")
    
    if not APP_ID or not APP_SECRET:
        raise Exception("请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
    
    sync = FeishuBitableSync(APP_ID, APP_SECRET)
    
    # 创建表格
    table_id = create_bitable_table(sync, args.app_token, args.table_name, df)
    
    # 导入数据
    print(f"开始导入数据...")
    stats = sync.sync(df, args.app_token, table_id, mode="append")
    
    print("\n🎉 完成!")
    print(f"- 表格 ID: {table_id}")
    print(f"- 导入: {stats['created']} 条")
    print(f"- 自动创建字段: {stats['fields_created']} 个")
    print(f"\n分享链接: https://pangeedoc.feishu.cn/drive/base/{args.app_token}?table={table_id}")


if __name__ == "__main__":
    main()
