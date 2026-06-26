#!/usr/bin/env python3
"""
AI自动扩充方言词库（每日定时版）

调用 MiniMax AI 生成普通话→哈尔滨话新词，去重后写入本地库+云端 bitable

使用方式：
    python3 auto_enrich.py              # 生成并写入
    python3 auto_enrich.py --dry-run    # 仅预览，不写入
    python3 auto_enrich.py --count 20   # 指定生成数量（默认10条）
"""

import os, sys, re, json, urllib.request, sqlite3
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "data", "dialect.db")
CONFIG_YAML = os.path.join(SCRIPT_DIR, "data", "config.yaml")
LOG_FILE = os.path.join(SCRIPT_DIR, "memory", "auto_enrich.md")

BASE_URL = "https://api.minimaxi.com/anthropic/v1"
MODEL = "MiniMax-M2.7"

# ====== 读取 MiniMax API Key（从 openclaw.json 掩码或环境变量）======
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
if not API_KEY:
    try:
        import re as re2
        with open("/root/.openclaw/openclaw.json") as f:
            raw = f.read()
        keys = re2.findall(r'"apiKey":\s*"([^"]+)"', raw)
        for k in keys:
            if not k.startswith("__"):
                API_KEY = k
                break
    except Exception:
        pass

# ====== 读取飞书配置 ======
import yaml
_cfg = yaml.safe_load(open(CONFIG_YAML))
feishu_cfg = _cfg.get("feishu", {})
bitable_cfg = _cfg.get("bitable", {})
cloud_cfg = _cfg.get("cloud_share", {})

FEISHU_APP_ID = feishu_cfg.get("app_id", "")
FEISHU_APP_SECRET = feishu_cfg.get("app_secret", "")
BITABLE_APP_TOKEN = bitable_cfg.get("app_token", "")
BITABLE_TABLE_ID = bitable_cfg.get("table_id", "")
BITABLE_API = "https://open.feishu.cn/open-apis/bitable/v1/apps/" + BITABLE_APP_TOKEN + "/tables/" + BITABLE_TABLE_ID + "/records"


def load_existing_pairs():
    """加载本地已存在的 (普通话, 哈尔滨话) 对，避免重复写入"""
    if not os.path.exists(DB_PATH):
        return set()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT standard_word, dialect_word FROM dialect_map WHERE dialect_name='哈尔滨话'")
    pairs = set()
    for std, dial in c.fetchall():
        pairs.add((std.strip(), dial.strip()))
    conn.close()
    return pairs


def get_contributor():
    """从 config.yaml 的 bot_name 字段读取贡献者名称"""
    try:
        name = feishu_cfg.get("bot_name", "")
        if name and not name.startswith("<"):
            return name
    except Exception:
        pass
    return "智多虾"


def generate_new_pairs(count=10, existing_pairs=None):
    """调用 MiniMax AI 生成新的哈尔滨话方言词对"""
    if existing_pairs is None:
        existing_pairs = set()

    avoid_text = ""
    if existing_pairs:
        avoid_text = "\n\n以下词对本地库已有，请勿重复生成：\n" + str(list(existing_pairs))[:500]

    prompt = (
        "你是一个哈尔滨话（东北官话，哈尔滨地区）方言专家。请生成" + str(count) + "个日常生活中常用的普通话词语及其对应的哈尔滨话表达。\n\n"
        "要求：\n"
        "1. 必须是哈尔滨地区使用的方言词汇，不是其他东北地区（如辽宁、吉林）\n"
        "2. 每个词要常见、有趣、不同于普通话\n"
        "3. 每条包含：普通话词语、哈尔滨话说法、词性（动词/形容词/名词/副词/日常用语之一）\n"
        "4. 必须全部是本地库没有的\n"
        "5. 直接返回JSON数组，不要有其他内容：\n\n"
        "[\n"
        '  {"standard": "普通话", "dialect": "哈尔滨话", "category": "词性"},\n'
        "  ...\n"
        "]\n" + avoid_text
    )

    if not API_KEY:
        print("❌ 未找到有效的 MiniMax API Key")
        print("   请确保环境变量 MINIMAX_API_KEY 已设置，或 /root/.openclaw/openclaw.json 中有配置")
        return []

    payload = {
        "model": MODEL,
        "max_tokens": 3000,
        "messages": [{"role": "user", "content": prompt}]
    }

    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        BASE_URL + "/messages",
        data=data,
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read())

    text = ""
    for item in resp.get("content", []):
        if item.get("type") == "text":
            text = item.get("text", "")
            break

    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*$", "", text).strip()

    try:
        return json.loads(text)
    except Exception:
        matches = re.findall(
            r'\{\s*"standard"\s*:\s*"([^"]+)"\s*,\s*"dialect"\s*:\s*"([^"]+)"\s*,\s*"category"\s*:\s*"([^"]+)"\s*\}',
            text
        )
        return [{"standard": m[0], "dialect": m[1], "category": m[2]} for m in matches]


def get_token():
    """获取飞书 tenant_access_token"""
    data = json.dumps({"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())
    return resp.get("tenant_access_token", "")


def write_to_cloud(new_words, dry_run=False):
    """写入云端 bitable"""
    if not cloud_cfg.get("enabled", False):
        print("  ⚠️ 云端共享未开启，跳过")
        return 0

    token = get_token()
    if not token:
        print("  ❌ 无法获取飞书 token")
        return 0

    contributor = get_contributor()
    # 当天零点时间戳（毫秒），写入添加日期字段
    add_date_ms = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)
    synced = 0

    for item in new_words:
        if dry_run:
            print("  [云端预览] " + item["standard"] + " -> " + item["dialect"])
            synced += 1
            continue

        payload = {
            "fields": {
                "普通话": item["standard"],
                "哈尔滨话": item["dialect"],
                "词性": item["category"],
                "补充人": contributor,
                "备注": "AI自动扩充",
                "添加日期": add_date_ms,
            }
        }

        req = urllib.request.Request(
            BITABLE_API,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as r:
                result = json.loads(r.read())
            if result.get("code") == 0:
                print("  ☁️ 云端写入: " + item["standard"] + " -> " + item["dialect"])
                synced += 1
            else:
                print("  ⚠️ 云端失败: " + str(result.get("msg")))
        except Exception as e:
            print("  ❌ 云端异常: " + str(e))

    return synced


def write_log(new_words, total_generated, cloud_synced, mode):
    """写入日志"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n\n## " + now + " · AI自动扩充（" + mode + "）\n\n")
        f.write("- AI生成: " + str(total_generated) + " 条\n")
        f.write("- 去重后新增: " + str(len(new_words)) + " 条\n")
        f.write("- 云端写入: " + str(cloud_synced) + " 条\n")
        if new_words:
            f.write("- 新增词条:\n")
            for item in new_words:
                f.write("  - " + item["standard"] + " -> " + item["dialect"] + " (" + item["category"] + ")\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI自动扩充方言词库")
    parser.add_argument("--count", type=int, default=10, help="生成数量")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不写入")
    args = parser.parse_args()

    mode = "预览" if args.dry_run else "写入"
    print("=" * 50)
    print("🤖 AI自动扩充方言词库")
    print("=" * 50)
    print("模式: " + mode + "，生成数量: " + str(args.count))
    print("-" * 50)

    print("📖 加载本地已有词对...")
    existing_pairs = load_existing_pairs()
    print("   本地已有: " + str(len(existing_pairs)) + " 对")

    print("\n🤖 调用AI生成 " + str(args.count) + " 条新词...")
    generated = generate_new_pairs(count=args.count, existing_pairs=existing_pairs)
    print("   AI返回: " + str(len(generated)) + " 条")

    if not generated:
        print("❌ AI未返回有效数据")
        return

    new_items = []
    for item in generated:
        std = item.get("standard", "").strip()
        dial = item.get("dialect", "").strip()
        cat = item.get("category", "其他").strip()
        if not std or not dial:
            continue
        if (std, dial) in existing_pairs:
            print("   ⏭️ 跳过（本地已有）: " + std + " -> " + dial)
            continue
        if std == dial:
            continue
        new_items.append({"standard": std, "dialect": dial, "category": cat})
        print("   ✅ 新词: " + std + " -> " + dial + " (" + cat + ")")

    print("\n去重后新增: " + str(len(new_items)) + " 条")
    if not new_items:
        print("⚠️ 没有新词")
        return

    # 写入本地 SQLite
    if not args.dry_run:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for item in new_items:
            cursor.execute(
                "INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES (?, ?, ?, ?, ?)",
                ("哈尔滨话", item["category"], item["standard"], item["dialect"], "AI自动扩充")
            )
        conn.commit()
        conn.close()
        print("✅ 本地数据库写入完成")

    # 写入云端 bitable
    print("\n☁️ 写入云端...")
    cloud_synced = write_to_cloud(new_items, dry_run=args.dry_run)

    if not args.dry_run:
        write_log(new_items, len(generated), cloud_synced, mode)

    print("\n" + "=" * 50)
    print("🎉 完成！新增 " + str(len(new_items)) + " 条（云端 " + str(cloud_synced) + " 条）")
    if args.dry_run:
        print("   预览模式，未写入")
    print("=" * 50)


if __name__ == "__main__":
    main()
