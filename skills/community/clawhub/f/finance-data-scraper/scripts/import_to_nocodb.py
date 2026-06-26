#!/usr/bin/env python3
"""
批量导入财经导读数据到 NocoDB
读取 JSON 文件并逐条插入，支持去重检查
"""

import json
import sys
import requests
from pathlib import Path

# NocoDB 配置 - UAT 环境
BASE_URL = "https://nocodb.dixchain.com/api/v2"
TOKEN = "TNejcEzKlX92OU0tfp3NW9PDelevPvBadZ0j-A-3"
TABLE_ID = "m2w6ubg16mcn33m"  # UAT 环境表

HEADERS = {
    "xc-token": TOKEN,
    "Content-Type": "application/json"
}

def load_json_file(filepath):
    """加载 JSON 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_existing_records():
    """获取现有记录，用于去重（按 source+content 组合去重）"""
    url = f"{BASE_URL}/tables/{TABLE_ID}/records"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        records = data.get("list", [])
        
        # 提取 source+content 组合用于去重
        existing_keys = set()
        for rec in records:
            source = rec.get("source", "")
            content = rec.get("content", "")
            if source and content:
                # 按 source+content 组合去重
                existing_keys.add(f"{source}|||{content}")
        
        return existing_keys
    except requests.exceptions.RequestException as e:
        print(f"⚠️ 获取现有记录失败：{e}")
        return set()

def create_record(data):
    """创建单条记录"""
    url = f"{BASE_URL}/tables/{TABLE_ID}/records"
    
    try:
        response = requests.post(url, headers=HEADERS, json=data, timeout=30)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)

def batch_import(filepath):
    """批量导入"""
    print(f"📂 加载文件：{filepath}")
    data = load_json_file(filepath)
    
    records = data.get("records", [])
    metadata = data.get("metadata", {})
    
    print(f"📊 文件共 {len(records)} 条记录")
    print(f"📅 提取时间：{metadata.get('extracted_at', 'unknown')}")
    print()
    
    # 获取现有记录用于去重
    print("🔍 获取现有记录用于去重...")
    existing_contents = get_existing_records()
    print(f"📚 数据库现有 {len(existing_contents)} 条记录")
    print()
    
    success = 0
    failed = 0
    skipped = 0  # 因重复跳过
    
    for i, record in enumerate(records, 1):
        source = record.get("source", "")
        content = record.get("content", "")
        
        # 去重检查（按 source+content 组合去重）
        record_key = f"{source}|||{content}"
        if record_key in existing_contents:
            skipped += 1
            print(f"⏭️  [{i}/{len(records)}] 跳过（重复）: [{source}] {content[:30]}...")
            continue
        
        ok, result = create_record(record)
        
        if ok:
            success += 1
            existing_contents.add(record_key)  # 添加到已存在集合（防止同一文件内重复）
            print(f"✅ [{i}/{len(records)}] [{source}] {content[:30]}...")
        else:
            failed += 1
            # 检查是否是重复插入导致的失败（唯一约束冲突）
            error_msg = str(result).lower()
            if "duplicate" in error_msg or "unique" in error_msg or "conflict" in error_msg:
                skipped += 1
                print(f"⏭️  [{i}/{len(records)}] 跳过（数据库重复）: [{source}] {content[:30]}...")
            else:
                print(f"❌ [{i}/{len(records)}] 失败：{result}")
        
        # 避免请求过快
        import time
        time.sleep(0.2)
    
    print()
    print("=" * 60)
    print(f"✅ 成功插入：{success} 条")
    print(f"❌ 失败：{failed} 条")
    print(f"⏭️  跳过（重复）: {skipped} 条")
    if len(records) > 0:
        print(f"📈 成功率：{(success/len(records)*100):.1f}%")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        # 默认使用最新的文件
        data_dir = Path.home() / ".openclaw" / "workspace" / "projects" / "eastmoney-cjdd" / "data"
        json_files = sorted(data_dir.glob("dfcf_*.json"))
        
        if not json_files:
            print("❌ 未找到数据文件")
            print("用法：python3 import_to_nocodb.py <文件路径>")
            return
        
        filepath = json_files[-1]
        print(f"使用最新文件：{filepath}")
    else:
        filepath = Path(sys.argv[1])
    
    if not filepath.exists():
        print(f"❌ 文件不存在：{filepath}")
        return
    
    batch_import(filepath)

if __name__ == "__main__":
    main()
