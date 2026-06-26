#!/usr/bin/env python3
"""
BigSeed — 种子数据管理脚本

用法:
  python3 scripts/bigseed.py add --content "..." [--image path] [--tags tag1,tag2]
  python3 scripts/bigseed.py query [--from DATE] [--to DATE] [--type 感悟] [--emotion 温暖]
  python3 scripts/bigseed.py portrait
  python3 scripts/bigseed.py seeds-for-story [--from DATE] [--to DATE] [--limit 20]
  python3 scripts/bigseed.py stats [--from DATE] [--to DATE]
"""

import json, os, sys, uuid, argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

TZ = timezone(timedelta(hours=8))
DATA_DIR = Path(__file__).resolve().parent.parent / "memory" / "bigseed-data"
SEEDS_FILE = DATA_DIR / "seeds.json"
PORTRAIT_FILE = DATA_DIR / "portrait.json"
STORIES_FILE = DATA_DIR / "stories.json"

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default or ({} if path.suffix == ".json" and "seeds" not in path.name else {"seeds": []})

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def now_str():
    return datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")

def parse_date(s):
    """Parse YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS into datetime."""
    if not s:
        return None
    try:
        if "T" in s or " " in s:
            s = s.replace(" ", "T")
            if "+" in s or "Z" in s:
                return datetime.fromisoformat(s)
            return datetime.fromisoformat(s).replace(tzinfo=TZ)
        return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=TZ)
    except:
        return None

def cmd_add(args):
    ensure_data_dir()
    data = load_json(SEEDS_FILE)
    
    seed = {
        "id": str(uuid.uuid4()),
        "timestamp": now_str(),
        "content": args.content,
        "type": args.type or "日常",
        "emotion": args.emotion or "平静",
        "tags": [t.strip() for t in (args.tags or "").split(",") if t.strip()],
        "attachments": ([args.image] if args.image else [])
    }
    
    data.setdefault("seeds", []).insert(0, seed)
    save_json(SEEDS_FILE, data)
    
    print(f"✅ 种子已保存 ({len(data['seeds'])} 颗总数)")
    print(f"   ID: {seed['id']}")
    print(f"   内容: {seed['content'][:60]}")
    return seed

def cmd_query(args):
    data = load_json(SEEDS_FILE)
    seeds = data.get("seeds", [])
    
    date_from = parse_date(args.from_date)
    date_to = parse_date(args.to_date)
    
    results = []
    for s in seeds:
        ts = parse_date(s.get("timestamp", ""))
        if date_from and ts and ts < date_from:
            continue
        if date_to and ts and ts > date_to:
            continue
        if args.type and s.get("type") != args.type:
            continue
        if args.emotion and s.get("emotion") != args.emotion:
            continue
        results.append(s)
    
    print(f"📊 共 {len(results)} 条结果（总 {len(seeds)} 颗种子）")
    for s in results:
        print(f"\n  [{s.get('type','?')}] {s.get('emotion','')} {s.get('timestamp','')}")
        print(f"  {s.get('content','')[:80]}")
        if s.get("tags"):
            print(f"  #{' #'.join(s['tags'])}")
    return results

def cmd_portrait(args):
    ensure_data_dir()
    portrait = load_json(PORTRAIT_FILE)
    if not portrait:
        print("📭 暂无画像数据")
        return portrait
    print(json.dumps(portrait, ensure_ascii=False, indent=2))
    return portrait

def cmd_seeds_for_story(args):
    """输出种子数据供模型生成故事（JSON格式）"""
    data = load_json(SEEDS_FILE)
    seeds = data.get("seeds", [])
    
    date_from = parse_date(args.from_date)
    date_to = parse_date(args.to_date)
    limit = args.limit or 20
    
    results = []
    for s in seeds:
        ts = parse_date(s.get("timestamp", ""))
        if date_from and ts and ts < date_from:
            continue
        if date_to and ts and ts > date_to:
            continue
        results.append(s)
        if limit and len(results) >= limit:
            break
    
    # Also load portrait
    portrait = load_json(PORTRAIT_FILE)
    
    output = {
        "seed_count": len(results),
        "seeds": results,
        "portrait": portrait or {}
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return output

def cmd_stats(args):
    data = load_json(SEEDS_FILE)
    seeds = data.get("seeds", [])
    
    date_from = parse_date(args.from_date)
    date_to = parse_date(args.to_date)
    
    filtered = []
    for s in seeds:
        ts = parse_date(s.get("timestamp", ""))
        if date_from and ts and ts < date_from:
            continue
        if date_to and ts and ts > date_to:
            continue
        filtered.append(s)
    
    # Type distribution
    type_dist = {}
    emotion_dist = {}
    all_tags = {}
    
    for s in filtered:
        t = s.get("type", "其他")
        type_dist[t] = type_dist.get(t, 0) + 1
        e = s.get("emotion", "其他")
        emotion_dist[e] = emotion_dist.get(e, 0) + 1
        for tag in s.get("tags", []):
            all_tags[tag] = all_tags.get(tag, 0) + 1
    
    print(f"📊 种子统计")
    print(f"\n  总数: {len(filtered)} (总 {len(seeds)})")
    print(f"\n  📂 类型分布:")
    for t, c in sorted(type_dist.items(), key=lambda x: -x[1]):
        print(f"    {t}: {c}")
    print(f"\n  💭 情绪分布:")
    for e, c in sorted(emotion_dist.items(), key=lambda x: -x[1]):
        print(f"    {e}: {c}")
    if all_tags:
        print(f"\n  🏷 热门标签:")
        for tag, c in sorted(all_tags.items(), key=lambda x: -x[1])[:10]:
            print(f"    #{tag}: {c}")
    
    return len(filtered)

def main():
    parser = argparse.ArgumentParser(description="BigSeed 种子管理")
    sub = parser.add_subparsers(dest="command")
    
    # add
    p_add = sub.add_parser("add", help="新增种子")
    p_add.add_argument("--content", required=True)
    p_add.add_argument("--image")
    p_add.add_argument("--tags")
    p_add.add_argument("--type")
    p_add.add_argument("--emotion")
    
    # query
    p_q = sub.add_parser("query", help="查询种子")
    p_q.add_argument("--from", dest="from_date")
    p_q.add_argument("--to", dest="to_date")
    p_q.add_argument("--type")
    p_q.add_argument("--emotion")
    
    # portrait
    sub.add_parser("portrait", help="查看画像")
    
    # seeds-for-story
    p_sfs = sub.add_parser("seeds-for-story", help="输出种子数据供生成故事")
    p_sfs.add_argument("--from", dest="from_date")
    p_sfs.add_argument("--to", dest="to_date")
    p_sfs.add_argument("--limit", type=int, default=20)
    
    # stats
    p_st = sub.add_parser("stats", help="统计数据")
    p_st.add_argument("--from", dest="from_date")
    p_st.add_argument("--to", dest="to_date")
    
    args = parser.parse_args()
    
    if args.command == "add":
        cmd_add(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "portrait":
        cmd_portrait(args)
    elif args.command == "seeds-for-story":
        cmd_seeds_for_story(args)
    elif args.command == "stats":
        cmd_stats(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
