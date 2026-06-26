"""
cfc 知识图谱查询脚本
快速查询消金公司合作机构关系

用法:
  python3 query_cfc.py                    # 显示统计
  python3 query_cfc.py 河北银海            # 查询某机构合作哪些消金
  python3 query_cfc.py --company 中邮消费金融  # 查询某消金的所有合作机构
  python3 query_cfc.py --type 催收           # 查看某类型的合作机构列表
  python3 query_cfc.py --stat              # 显示 ontology 统计
"""
import json
import re
import argparse
from pathlib import Path
from collections import defaultdict

GRAPH = Path(__file__).parent.parent.parent / "memory" / "ontology" / "graph.jsonl"

# 关系类型 → 中文标签
REL_LABELS = {
    "cooperates_with": "合作",
    "publishes_disclosure": "发布披露",
    "includes_company": "包含",
    "disclosed_by": "披露主体",
    "appears_in_document": "出现于",
}

# 公司类型 → 中文
CO_TYPE_LABELS = {
    "LawFirm": "律所",
    "TechCompany": "科技公司",
    "CollectionBPO": "催收BPO",
    "GuaranteeCompany": "融资担保",
    "FinancialInstitution": "金融机构",
    "Unknown": "其他",
    # 兼容 category 字段的中文值（来自结构化JSON）
    "催收机构-律所": "律所",
    "催收机构-科技": "科技公司",
    "催收机构-商务": "催收BPO",
    "催收机构": "催收BPO",
    "催收合作机构": "催收BPO",
    "": "其他",
    "?": "其他",
}


def load_graph():
    """加载 graph.jsonl，返回 (entities, relations) 元组列表。"""
    entities = {}  # id -> entity dict
    relations = []  # list of relation dicts
    with open(GRAPH) as f:
        for line in f:
            d = json.loads(line)
            if d.get("op") == "create":
                e = d["entity"]
                entities[e["id"]] = e
            elif d.get("op") == "relate":
                relations.append(d)
    return entities, relations


def query_by_name(name: str, entities: dict, relations: list):
    """按机构名查询，返回所有相关公司+关系。"""
    results = []
    for eid, e in entities.items():
        p = e.get("properties", {})
        if name in p.get("name", ""):
            results.append((eid, e))
    return results


def query_company_cooperations(co_name: str, entities: dict, relations: list):
    """查询某消金公司的所有合作机构，按类型分组。"""
    co_id = None
    match_name = None
    # 优先精确匹配 Company 类型
    for eid, e in entities.items():
        if e.get("type") == "Company" and e.get("properties", {}).get("name", "") == co_name:
            co_id = eid
            match_name = co_name
            break
    if not co_id:
        # 模糊匹配：包含查询词，优先 Company 其次 DisclosureList
        candidates = [(eid, e) for eid, e in entities.items()
                     if co_name in e.get("properties", {}).get("name", "")]
        # 优先 Company
        for eid, e in candidates:
            if e.get("type") == "Company":
                co_id = eid
                match_name = e.get("properties", {}).get("name", "")
                break
        if not co_id and candidates:
            eid, e = candidates[0]
            co_id = eid
            match_name = e.get("properties", {}).get("name", "")
        if match_name:
            print(f"  (匹配到: {match_name})")
    
    if not co_id:
        print(f"未找到公司: {co_name}")
        return

    # 找所有与该公司合作的关系
    by_type = defaultdict(list)
    for r in relations:
        if r.get("from") == co_id or r.get("to") == co_id:
            if r.get("rel") == "cooperates_with":
                other_id = r.get("to") if r.get("from") == co_id else r.get("from")
                other = entities.get(other_id, {})
                other_p = other.get("properties", {})
                dtype = other_p.get("disclosure_type", "?")
                ctype = other_p.get("company_type", other_p.get("category", "?"))
                phone = other_p.get("phone", "")
                by_type[dtype].append({
                    "id": other_id,
                    "name": other_p.get("name", "?"),
                    "type": ctype,
                    "phone": phone,
                    "collected_at": other_p.get("collected_at", "")[:10] if other_p.get("collected_at") else "",
                })

    print(f"\n{'='*60}")
    print(f"  {co_name} 合作机构查询")
    print(f"{'='*60}")
    total = 0
    for dtype, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
        print(f"\n[{dtype}] ({len(items)}家)")
        for item in sorted(items, key=lambda x: x["name"]):
            ctype = CO_TYPE_LABELS.get(item["type"], item["type"])
            phone = f" | {item['phone']}" if item["phone"] else ""
            print(f"  {item['name']} ({ctype}){phone}")
        total += len(items)
    print(f"\n共 {total} 家合作机构")


def query_agency_cooperations(agency_name: str, entities: dict, relations: list):
    """查询某合作机构合作的消金公司。"""
    # 找机构ID
    agency_ids = []
    for eid, e in entities.items():
        if agency_name in e.get("properties", {}).get("name", ""):
            agency_ids.append(eid)
    
    if not agency_ids:
        print(f"未找到机构: {agency_name}")
        return

    print(f"\n{'='*60}")
    print(f"  '{agency_name}' 合作机构查询")
    print(f"{'='*60}")

    for aid in agency_ids:
        aid_p = entities[aid].get("properties", {})
        print(f"\n机构: {aid_p.get('name', aid)}")
        print(f"类型: {CO_TYPE_LABELS.get(aid_p.get('company_type', aid_p.get('category','?')), aid_p.get('company_type', aid_p.get('category','?')))}")
        print(f"来源: {aid_p.get('source_company','')} | {aid_p.get('disclosure_type','')}")
        if aid_p.get('phone'):
            print(f"电话: {aid_p.get('phone')}")

        # 找合作消金（both directions）
        for r in relations:
            is_from = r.get("from") == aid
            is_to = r.get("to") == aid
            if (is_from or is_to) and r.get("rel") == "cooperates_with":
                co_id = r.get("to") if is_from else r.get("from")
                co_p = entities.get(co_id, {}).get("properties", {})
                rel_p = r.get("properties", {})
                print(f"\n  → 合作: {co_p.get('name', co_id)}")
                print(f"     类型: {rel_p.get('cooperation_type','')}")
                print(f"     披露日期: {rel_p.get('disclosure_date','')}")


def show_stats(entities: dict, relations: list):
    """显示 ontology 统计信息。"""
    companies = [e for e in entities.values() if e.get("type") == "Company"]
    docs = [e for e in entities.values() if e.get("type") == "DisclosureDocument"]
    lists = [e for e in entities.values() if e.get("type") == "DisclosureList"]
    
    # 按 source_company 统计
    from collections import Counter
    co_counter = Counter()
    type_counter = Counter()
    for c in companies:
        p = c.get("properties", {})
        if p.get("source_company"):
            co_counter[p["source_company"]] += 1
        type_counter[p.get("company_type", "?")] += 1

    print(f"\n{'='*60}")
    print(f"  cfc 知识图谱统计")
    print(f"{'='*60}")
    print(f"  总实体: {len(entities)}")
    print(f"  总关系: {len(relations)}")
    print(f"  合作机构: {len(companies)}")
    print(f"  披露文档: {len(docs)}")
    print(f"  披露清单: {len(lists)}")
    print(f"\n  机构类型分布:")
    for t, cnt in type_counter.most_common():
        label = CO_TYPE_LABELS.get(t, t)
        print(f"    {label}: {cnt}")
    print(f"\n  覆盖公司（前15）:")
    for co, cnt in co_counter.most_common(15):
        print(f"    {co}: {cnt}")


def show_recent(entities: dict, relations: list, limit: int = 20):
    """显示最近入库的数据。"""
    # 找有 inserted_at 的实体
    recent = []
    for eid, e in entities.items():
        p = e.get("properties", {})
        ia = p.get("inserted_at", "")
        if ia:
            recent.append((ia, eid, e))
    
    recent.sort(reverse=True)
    
    print(f"\n最近入库 ({limit}条):")
    for ia, eid, e in recent[:limit]:
        p = e.get("properties", {})
        print(f"  [{ia[:19]}] {p.get('name', eid)[:40]} ({e.get('type','')})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", help="机构名称（模糊匹配）")
    parser.add_argument("--company", type=str, help="查询某消金公司的合作机构")
    parser.add_argument("--stat", action="store_true", help="显示统计信息")
    parser.add_argument("--recent", action="store_true", help="显示最近入库")
    args = parser.parse_args()

    entities, relations = load_graph()

    if args.stat:
        show_stats(entities, relations)
    elif args.recent:
        show_recent(entities, relations)
    elif args.company:
        query_company_cooperations(args.company, entities, relations)
    elif args.name:
        # 优先当消金公司查，次优先当合作机构查
        # 先看 entities 里有没有叫这个名的（可能是消金公司）
        found_as_co = False
        for eid, e in entities.items():
            if e.get("properties", {}).get("name", "") == args.name:
                # 可能是消金公司
                is_cfc = any(r.get("from") == eid or r.get("to") == eid 
                            for r in relations if r.get("rel") == "publishes_disclosure")
                if is_cfc or e.get("type") == "Company":
                    query_company_cooperations(args.name, entities, relations)
                    found_as_co = True
                    break
        if not found_as_co:
            query_agency_cooperations(args.name, entities, relations)
    else:
        show_stats(entities, relations)
        show_recent(entities, relations, limit=10)
