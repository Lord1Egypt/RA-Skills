#!/usr/bin/env python3
"""
BigLead — 客户线索数据管理

用法:
  python3 skills/biglead/scripts/biglead.py add --company "公司名" [--business ...] [--region ...] [--industry ...] [--website ...] [--phone ...] [--email ...] [--source ...]
  python3 skills/biglead/scripts/biglead.py import --file leads.json
  python3 skills/biglead/scripts/biglead.py query [--industry 行业] [--region 地区] [--status new]
  python3 skills/biglead/scripts/biglead.py update --id <uuid> [--status new|contacted|qualified|disqualified] [--notes "..."]
  python3 skills/biglead/scripts/biglead.py export [--output leads.csv]
  python3 skills/biglead/scripts/biglead.py stats
  python3 skills/biglead/scripts/biglead.py log-search --query "..." --results N --new N
  python3 skills/biglead/scripts/biglead.py check-dupes --company "公司名"
"""

import json, os, sys, uuid, csv, io, argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

TZ = timezone(timedelta(hours=8))
DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "memory" / "lead-data"
LEADS_FILE = DATA_DIR / "leads.json"
HISTORY_FILE = DATA_DIR / "search-history.json"
EXPORT_DIR = DATA_DIR / "export"

def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def load_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        if default is not None:
            return default
        return {"leads": []}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def now_str():
    return datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")

def cmd_add(args):
    ensure_dirs()
    data = load_json(LEADS_FILE, {"leads": []})

    # Check for duplicates
    dupes = check_duplicates(data["leads"], args.company)
    if dupes:
        print(f"⚠️  公司 \"{args.company}\" 已存在（{len(dupes)} 条匹配）:")
        for d in dupes:
            print(f"   [{d['id'][:8]}] {d['company']} | {d.get('region','?')} | {d.get('status','new')}")
        print(f"  使用 update 更新已有线索，或确认不重复再添加")
        return

    sources = []
    if args.source:
        sources.append({"name": args.source, "url": args.source_url or "", "trusted": True})

    lead = {
        "id": str(uuid.uuid4()),
        "company": args.company,
        "business": args.business or "",
        "region": args.region or "",
        "industry": args.industry or "",
        "website": args.website or "",
        "phone": args.phone or "",
        "email": args.email or "",
        "address": args.address or "",
        "sources": sources,
        "credibility": min(len(sources), 3),
        "status": "new",
        "created_at": now_str(),
        "updated_at": now_str(),
        "notes": ""
    }

    data["leads"].insert(0, lead)
    save_json(LEADS_FILE, data)

    print(f"✅ 线索已保存 (共 {len(data['leads'])} 条)")
    print(f"   ID: {lead['id']}")
    print(f"   公司: {lead['company']}")
    if lead.get("phone"):
        print(f"   📞 {lead['phone']}")
    if lead.get("email"):
        print(f"   ✉️ {lead['email']}")
    print(f"   可信度: {'█' * lead['credibility']}{'░' * (3 - lead['credibility'])} ({lead['credibility']}/3)")
    return lead

def check_duplicates(leads, company_name):
    """Check if company already exists (fuzzy match)."""
    if not company_name:
        return []
    keywords = set(company_name.lower().replace("（", "(").replace("）", ")").replace("有限", "").replace("公司", "").split())
    matches = []
    for lead in leads:
        lead_kw = set(lead.get("company", "").lower().replace("（", "(").replace("）", ")").replace("有限", "").replace("公司", "").split())
        overlap = keywords & lead_kw
        if len(overlap) >= 2 or company_name[:4].lower() in lead.get("company", "").lower():
            matches.append(lead)
    return matches

def cmd_import(args):
    ensure_dirs()
    try:
        with open(args.file) as f:
            imported = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ 无法读取文件: {e}")
        return

    data = load_json(LEADS_FILE, {"leads": []})
    count = 0
    for item in imported.get("leads", [imported] if isinstance(imported, dict) else []):
        item.setdefault("id", str(uuid.uuid4()))
        item.setdefault("status", "new")
        item.setdefault("sources", [])
        item.setdefault("credibility", 0)
        item.setdefault("created_at", now_str())
        item.setdefault("updated_at", now_str())
        for field in ("company", "business", "region", "industry", "website", "phone", "email", "address", "notes"):
            item.setdefault(field, "")
        # Dedup check
        if not check_duplicates(data["leads"], item.get("company", "")):
            data["leads"].insert(0, item)
            count += 1

    save_json(LEADS_FILE, data)
    print(f"✅ 导入完成：新增 {count} 条，跳过重复，总计 {len(data['leads'])} 条")

def cmd_query(args):
    data = load_json(LEADS_FILE, {"leads": []})
    results = data["leads"]

    if args.industry:
        results = [r for r in results if args.industry.lower() in r.get("industry", "").lower()]
    if args.region:
        results = [r for r in results if args.region.lower() in r.get("region", "").lower()]
    if args.status:
        results = [r for r in results if r.get("status") == args.status]
    if args.company:
        results = [r for r in results if args.company.lower() in r.get("company", "").lower()]

    print(f"📊 共 {len(results)} 条线索（总 {len(data['leads'])} 条）")
    for r in results:
        cred_icon = "🟢" if r.get("credibility", 0) >= 2 else "🟡" if r.get("credibility", 0) >= 1 else "⚪"
        print(f"\n{cred_icon} [{r.get('status','?')}] {r.get('company','?')}")
        print(f"   业务: {r.get('business','?')}")
        if r.get("phone"):  print(f"   📞 {r['phone']}")
        if r.get("email"):  print(f"   ✉️ {r['email']}")
        if r.get("website"): print(f"   🌐 {r['website']}")
        print(f"   📍 {r.get('region','?')} | {r.get('industry','?')}")
        print(f"   可信度: {r.get('credibility',0)}/3 | 来源: {len(r.get('sources',[]))} | ID: {r.get('id','?')[:8]}")
    return results

def cmd_update(args):
    data = load_json(LEADS_FILE, {"leads": []})
    found = False
    for lead in data["leads"]:
        if lead["id"] == args.id:
            if args.status:
                lead["status"] = args.status
            if args.phone:
                lead["phone"] = args.phone
            if args.email:
                lead["email"] = args.email
            if args.notes:
                lead["notes"] = args.notes
            lead["updated_at"] = now_str()
            found = True
            print(f"✅ 已更新: {lead['company']} → status={lead['status']}")
            save_json(LEADS_FILE, data)
            break
    if not found:
        print(f"❌ 未找到 ID: {args.id}")

def cmd_export(args):
    data = load_json(LEADS_FILE, {"leads": []})
    output_path = args.output or str(EXPORT_DIR / f"leads-{datetime.now(TZ).strftime('%Y%m%d')}.csv")

    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["公司名", "业务", "地区", "行业", "官网", "电话", "邮箱", "地址", "可信度", "状态", "备注"])
        for r in data["leads"]:
            writer.writerow([
                r.get("company", ""),
                r.get("business", ""),
                r.get("region", ""),
                r.get("industry", ""),
                r.get("website", ""),
                r.get("phone", ""),
                r.get("email", ""),
                r.get("address", ""),
                r.get("credibility", 0),
                r.get("status", ""),
                r.get("notes", "")
            ])

    print(f"✅ 已导出 {len(data['leads'])} 条线索 → {output_path}")

def cmd_stats(args):
    data = load_json(LEADS_FILE, {"leads": []})
    leads = data["leads"]
    total = len(leads)

    status_dist = {}
    industry_dist = {}
    region_dist = {}
    cred_dist = {}
    has_phone = 0
    has_email = 0

    for r in leads:
        s = r.get("status", "unknown")
        status_dist[s] = status_dist.get(s, 0) + 1
        ind = r.get("industry", "未分类")
        industry_dist[ind] = industry_dist.get(ind, 0) + 1
        reg = r.get("region", "未知")
        region_dist[reg] = region_dist.get(reg, 0) + 1
        c = r.get("credibility", 0)
        cred_dist[c] = cred_dist.get(c, 0) + 1
        if r.get("phone"): has_phone += 1
        if r.get("email"): has_email += 1

    print(f"📊 BigLead 统计")
    print(f"\n   总线索: {total}")
    print(f"\n   📌 状态分布:")
    for s, c in sorted(status_dist.items(), key=lambda x: -x[1]):
        print(f"      {s}: {c}")
    print(f"\n   🏭 行业分布 (Top 5):")
    for ind, c in sorted(industry_dist.items(), key=lambda x: -x[1])[:5]:
        print(f"      {ind}: {c}")
    print(f"\n   📍 地区分布 (Top 5):")
    for reg, c in sorted(region_dist.items(), key=lambda x: -x[1])[:5]:
        print(f"      {reg}: {c}")
    print(f"\n   🎯 可信度:")
    for c in sorted(cred_dist.keys(), reverse=True):
        icon = "🟢" if c >= 2 else "🟡" if c >= 1 else "⚪"
        print(f"      {icon} {c}/3: {cred_dist[c]}")
    print(f"\n   📞 联系方式:")
    print(f"      有电话: {has_phone}/{total}")
    print(f"      有邮箱: {has_email}/{total}")

def cmd_log_search(args):
    ensure_dirs()
    history = load_json(HISTORY_FILE, {"searches": []})

    entry = {
        "timestamp": now_str(),
        "query": args.query,
        "results": int(args.results),
        "new_leads": int(args.new),
        "industry": args.industry or "",
        "region": args.region or ""
    }

    history.setdefault("searches", []).insert(0, entry)

    # Keep last 100
    if len(history["searches"]) > 100:
        history["searches"] = history["searches"][:100]

    save_json(HISTORY_FILE, history)
    print(f"✅ 搜索记录已保存: \"{args.query}\" → {args.results}条结果, {args.new}条新线索")

def cmd_existing(args):
    """输出已有关联名单，供搜索时过滤去重。"""
    data = load_json(LEADS_FILE, {"leads": []})
    results = data["leads"]

    if args.industry:
        results = [r for r in results if args.industry.lower() in r.get("industry", "").lower()]
    if args.region:
        results = [r for r in results if args.region.lower() in r.get("region", "").lower()]

    # 只输出公司名列表，方便模型直接拿去过滤
    names = [r.get("company", "") for r in results if r.get("company")]
    domains = [r.get("website", "") for r in results if r.get("website")]

    print(f"⚠️  该范围已有 {len(names)} 家公司（搜索时将自动过滤）")
    for n in names:
        print(f"   已收录: {n}")
    if domains:
        print(f"   已收录域名: {' '.join(domains)}")

    # 同时输出简短格式供脚本解析
    print(f"---EXISTING_START---")
    for n in names:
        print(n)
    print(f"---EXISTING_END---")
    return names


def cmd_check_dupes(args):
    data = load_json(LEADS_FILE, {"leads": []})
    matches = check_duplicates(data["leads"], args.company)
    if matches:
        print(f"⚠️  找到 {len(matches)} 条相似记录:")
        for m in matches:
            print(f"   [{m['id'][:8]}] {m['company']} | {m.get('region','')} | {m.get('status','')}")
    else:
        print(f"✅ 无重复记录")

def main():
    parser = argparse.ArgumentParser(description="BigLead 客户线索管理")
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="新增线索")
    p_add.add_argument("--company", required=True)
    p_add.add_argument("--business")
    p_add.add_argument("--region")
    p_add.add_argument("--industry")
    p_add.add_argument("--website")
    p_add.add_argument("--phone")
    p_add.add_argument("--email")
    p_add.add_argument("--address")
    p_add.add_argument("--source")
    p_add.add_argument("--source-url")

    # import
    p_imp = sub.add_parser("import", help="从 JSON 文件导入")
    p_imp.add_argument("--file", required=True)

    # query
    p_q = sub.add_parser("query", help="查询线索")
    p_q.add_argument("--industry")
    p_q.add_argument("--region")
    p_q.add_argument("--status")
    p_q.add_argument("--company")

    # update
    p_upd = sub.add_parser("update", help="更新线索")
    p_upd.add_argument("--id", required=True)
    p_upd.add_argument("--status", choices=["new", "contacted", "qualified", "disqualified"])
    p_upd.add_argument("--phone")
    p_upd.add_argument("--email")
    p_upd.add_argument("--notes")

    # export
    p_exp = sub.add_parser("export", help="导出 CSV")
    p_exp.add_argument("--output")

    # stats
    sub.add_parser("stats", help="统计")

    # log-search
    p_log = sub.add_parser("log-search", help="记录搜索历史")
    p_log.add_argument("--query", required=True)
    p_log.add_argument("--results", required=True)
    p_log.add_argument("--new", required=True)
    p_log.add_argument("--industry")
    p_log.add_argument("--region")

    # check-dupes
    p_dup = sub.add_parser("check-dupes", help="查重")
    p_dup.add_argument("--company", required=True)

    # existing
    p_exist = sub.add_parser("existing", help="查看已有公司名单（供搜索时过滤去重）")
    p_exist.add_argument("--industry")
    p_exist.add_argument("--region")

    args = parser.parse_args()

    commands = {
        "add": cmd_add,
        "import": cmd_import,
        "query": cmd_query,
        "update": cmd_update,
        "export": cmd_export,
        "stats": cmd_stats,
        "log-search": cmd_log_search,
        "check-dupes": cmd_check_dupes,
        "existing": cmd_existing,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
