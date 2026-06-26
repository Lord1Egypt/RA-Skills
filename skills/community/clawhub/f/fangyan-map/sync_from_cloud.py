#!/usr/bin/env python3
"""
从云端共享 bitable 拉取新词合并到本地数据库

增量逻辑：
- 每次同步后记录"本次最大添加日期"
- 下次同步时只拉取比该日期新的记录
- 支持 --full 强制全量拉取

使用方式：
    python3 sync_from_cloud.py              # 增量（只拉新词）
    python3 sync_from_cloud.py --full      # 全量（忽略增量状态）
    python3 sync_from_cloud.py --dry-run   # 预览模式
"""

import sys
import os
import json
import urllib.request
import sqlite3
import argparse
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "data", "dialect.db")
CURSOR_FILE = os.path.join(SCRIPT_DIR, "data", "sync_cursor.json")
MEMORY_DIR = os.path.join(SCRIPT_DIR, "memory")
CONFIG_YAML = os.path.join(SCRIPT_DIR, "data", "config.yaml")

import yaml
feishu_cfg = yaml.safe_load(open(CONFIG_YAML))['feishu']
bitable_cfg = yaml.safe_load(open(CONFIG_YAML))['bitable']

BITABLE_APP_TOKEN = bitable_cfg['app_token']
BITABLE_TABLE_ID = bitable_cfg['table_id']
BITABLE_API = "https://open.feishu.cn/open-apis/bitable/v1/apps/" + BITABLE_APP_TOKEN + "/tables/" + BITABLE_TABLE_ID + "/records"


def get_token():
    """获取飞书 tenant_access_token"""
    data = json.dumps({"app_id": feishu_cfg['app_id'], "app_secret": feishu_cfg['app_secret']}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())
    if resp.get('code') != 0:
        raise Exception("获取token失败: " + str(resp))
    return resp['tenant_access_token']


def load_cursor():
    """加载上次同步的光标（最大添加日期，毫秒时间戳）"""
    if os.path.exists(CURSOR_FILE):
        with open(CURSOR_FILE) as f:
            return json.load(f).get('max_add_date', 0)
    return 0


def save_cursor(max_add_date):
    """保存本次同步的最大添加日期"""
    with open(CURSOR_FILE, 'w') as f:
        json.dump({'max_add_date': max_add_date, 'updated_at': datetime.now().isoformat()}, f, ensure_ascii=False)


def fetch_records(token, min_add_date=0, limit=10000):
    """
    获取 bitable 记录（只返回添加日期 > min_add_date 的记录）
    min_add_date: 毫秒时间戳
    """
    records = []
    page_token = None
    total_fetched = 0

    while total_fetched < limit:
        page_size = min(100, limit - total_fetched)
        url = BITABLE_API + "?page_size=" + str(page_size)
        if page_token:
            url += "&page_token=" + page_token

        req = urllib.request.Request(
            url,
            headers={'Authorization': 'Bearer ' + token},
            method='GET'
        )

        with urllib.request.urlopen(req) as r:
            result = json.loads(r.read())

        if result.get('code') != 0:
            raise Exception("获取记录失败: " + result.get('msg'))

        items = result.get('data', {}).get('items', [])

        # 增量过滤
        for item in items:
            add_date_val = item.get('fields', {}).get('添加日期', 0)
            if add_date_val is None:
                add_date_val = 0
            if min_add_date == 0 or add_date_val > min_add_date:
                records.append(item)

        total_fetched += len(items)
        has_more = result.get('data', {}).get('has_more', False)
        page_token = result.get('data', {}).get('page_token')
        if not has_more:
            break
        if not items:
            break

    return records


def normalize_field(value):
    """规范化字段值"""
    if isinstance(value, list):
        return value[0].get('text', '') if value else ''
    return value or ''


def sync_to_local(records, dry_run=False):
    """同步记录到本地数据库"""
    if not os.path.exists(DB_PATH):
        print("❌ 数据库不存在: " + DB_PATH)
        print("请先运行: python3 init_db.py")
        return 0, 0, []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    synced = 0
    skipped = 0
    new_words = []

    for record in records:
        fields = record.get('fields', {})
        std_word = normalize_field(fields.get('普通话', ''))
        dial_word = normalize_field(fields.get('哈尔滨话', ''))
        category = normalize_field(fields.get('词性', '其他'))
        contributor = normalize_field(fields.get('补充人', ''))
        remark = normalize_field(fields.get('备注', ''))

        if not std_word or not dial_word:
            skipped += 1
            continue

        if dry_run:
            print("  [预览] " + std_word + " → " + dial_word + " (" + category + ") - " + contributor)
            synced += 1
            continue

        sql = "INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql, ('哈尔滨话', category, std_word, dial_word, remark))
        if cursor.rowcount > 0:
            synced += 1
            new_words.append((std_word, dial_word, category, contributor))
            print("✅ 新增: " + std_word + " → " + dial_word + " (" + category + ") - " + contributor)
        else:
            skipped += 1

    conn.commit()
    conn.close()

    return synced, skipped, new_words


def write_log(synced, skipped, new_words, total_online, mode):
    """写入同步日志"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    log_file = os.path.join(MEMORY_DIR, "sync_from_cloud.md")
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("\n\n## " + now + " · " + ("全量" if mode == "full" else "增量") + "同步\n\n")
        f.write("- 线上总记录: " + str(total_online) + " 条\n")
        f.write("- 本次获取: " + str(synced + skipped) + " 条\n")
        f.write("- 新增: " + str(synced) + " 条\n")
        f.write("- 跳过: " + str(skipped) + " 条\n")
        if new_words:
            f.write("- 新增词条:\n")
            for std, dial, cat, contrib in new_words:
                f.write("  - " + std + " → " + dial + " (" + cat + ") @" + contrib + "\n")


def main():
    parser = argparse.ArgumentParser(description='从云端同步方言词到本地')
    parser.add_argument('--full', action='store_true', help='全量拉取（忽略增量状态）')
    parser.add_argument('--dry-run', action='store_true', help='预览模式不写入')
    args = parser.parse_args()

    mode = 'full' if args.full else '增量'
    last_cursor = 0 if args.full else load_cursor()

    print("=" * 50)
    print("🔄 方言词云端同步工具")
    print("=" * 50)
    print("模式: " + ("预览" if args.dry_run else "写入") + " | " + mode)
    if last_cursor and not args.full:
        print("（增量，上次同步光标: " + str(last_cursor) + "）")
    print("目标: " + BITABLE_APP_TOKEN)
    print("-" * 50)

    try:
        print("📡 连接飞书...")
        token = get_token()
        if token is None:
            sys.exit(1)
        print("✅ 已获取凭证")

        print("📥 拉取云端记录...")
        records = fetch_records(token, min_add_date=last_cursor)
        print("📊 本次获取 " + str(len(records)) + " 条" + ("（增量）" if not args.full else "（全量）"))

        if not records:
            print("⚠️ 没有新记录要同步")
            return

        # 去重：相同 (普通话, 哈尔滨话) 只保留一条
        seen = {}
        for r in records:
            f = r.get('fields', {})
            std = normalize_field(f.get('普通话'))
            dial = normalize_field(f.get('哈尔滨话'))
            key = (std, dial)
            if key not in seen:
                seen[key] = r

        unique_records = list(seen.values())
        print("🔄 去重后: " + str(len(unique_records)) + " 条")

        # 计算本次最大添加日期
        max_add_date = last_cursor
        for r in unique_records:
            add_date_val = r.get('fields', {}).get('添加日期', 0)
            if add_date_val and add_date_val > max_add_date:
                max_add_date = int(add_date_val)

        # 同步到本地
        print("\n📝 同步到本地数据库...")
        synced, skipped, new_words = sync_to_local(unique_records, args.dry_run)

        # 更新光标
        if not args.dry_run and max_add_date > last_cursor:
            save_cursor(max_add_date)
            print("💾 已保存同步光标: " + str(max_add_date))

        # 统计
        if not args.dry_run:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM dialect_map WHERE dialect_name='哈尔滨话'")
            total_hb = c.fetchone()[0]
            conn.close()
        else:
            total_hb = -1

        print("\n" + "=" * 50)
        print("🎉 完成！")
        print("   模式: " + mode)
        print("   新增: " + str(synced) + " 条")
        print("   跳过: " + str(skipped) + " 条")
        if total_hb >= 0:
            print("   本地哈尔滨话词条总数: " + str(total_hb) + " 条")
        if args.dry_run:
            print("   预览模式，未实际写入")
        print("=" * 50)

        # 写日志
        if not args.dry_run:
            write_log(synced, skipped, new_words, len(records), mode)

    except Exception as e:
        print("❌ 错误: " + str(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
