#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""只读历史查询：文献证据 → 历史版本 → 现代出品 → 单变量创作简报。"""
import argparse
import collections
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
STATUSES = {"documented", "supported_secondary", "disputed", "unverified"}
KINDS = {"primary_transcription", "institutional_excerpt", "secondary", "catalog_only"}
LABELS = {"documented": "文献有记录", "supported_secondary": "二手研究支持",
          "disputed": "归属/说法有争议", "unverified": "尚未核实"}


def norm(text):
    return re.sub(r"[\s\-_·'’&]+", "", str(text)).casefold()


def load(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate(data, recipes):
    """验证证据链完整性，不把结构校验称为原文真实性验证。"""
    errors = []
    sources = data.get("sources", [])
    records = data.get("records", [])
    families = data.get("families", [])
    for label, items in (("source", sources), ("record", records), ("family", families)):
        ids = [item.get("id") for item in items]
        if not all(ids) or len(ids) != len(set(ids)):
            errors.append(f"{label} ID缺失/重复")
    src = {s.get("id"): s for s in sources}
    fam_ids = {f.get("id") for f in families}
    names = {r.get("name") for r in recipes}
    for s in sources:
        for key in ("title", "author", "edition", "url", "accessed", "verification"):
            if not s.get(key):
                errors.append(f"{s.get('id')} 来源缺 {key}")
        if s.get("kind") not in KINDS or not s.get("url", "").startswith("https://"):
            errors.append(f"{s.get('id')} 来源类型/URL非法")
        permitted = {"primary_transcription": {"text_checked"}, "institutional_excerpt": {"text_checked"},
                     "secondary": {"secondary_checked"}, "catalog_only": {"catalog_checked"}}
        if s.get("verification") not in permitted.get(s.get("kind"), set()):
            errors.append(f"{s.get('id')} verification与证据载体不一致")
    for r in records:
        rid = r.get("id")
        for key in ("name", "name_en", "summary", "origin_caution", "structure", "claims"):
            if not r.get(key):
                errors.append(f"{rid} 缺 {key}")
        if r.get("family_id") not in fam_ids:
            errors.append(f"{rid} 未知家族")
        if r.get("canonical_name") and r["canonical_name"] not in names:
            errors.append(f"{rid} 标准中文名未命中")
        profile = data.get("policy", {}).get("distribution_profile")
        for c in r.get("claims", []):
            if c.get("status") not in STATUSES:
                errors.append(f"{rid} 非法证据等级")
            if not c.get("text") or not c.get("source_ids") or not c.get("locator"):
                errors.append(f"{rid} 主张缺内容/来源/定位")
            for sid in c.get("source_ids", []):
                if sid not in src:
                    errors.append(f"{rid} 不存在的来源 {sid}")
            if profile == "clawhub_mit0":
                # 事实核查等级与「是否随包分发第三方表达」是两条独立链。
                if any(key in c for key in ("quote_en", "quote_zh", "method_original", "method_zh")):
                    errors.append(f"{rid} MIT-0版仍随包保存引文/逐句译文")
                ev = c.get("evidence_record")
                if (not isinstance(ev, dict) or ev.get("source_ids") != c.get("source_ids")
                        or not ev.get("locator") or not ev.get("verification_basis")
                        or ev.get("expression") != "independent_summary" or not c.get("summary")):
                    errors.append(f"{rid} 缺与来源一致的独立事实摘要证据记录")
            elif bool(c.get("quote_en")) != bool(c.get("quote_zh")):
                errors.append(f"{rid} 引文缺中英对照")
            checked = [src[sid] for sid in c.get("source_ids", []) if sid in src]
            if c.get("status") == "documented":
                if not any(s.get("kind") in ("primary_transcription", "institutional_excerpt") and s.get("verification") == "text_checked" for s in checked):
                    errors.append(f"{rid} documented 没有已读原文/机构摘录证据")
            if c.get("status") == "supported_secondary" and not any(s.get("kind") != "catalog_only" and s.get("verification") in ("text_checked", "secondary_checked") for s in checked):
                errors.append(f"{rid} 二手事实不能仅由书目支撑")
        for v in r.get("historical_versions", []):
            if v.get("source_id") not in src or not v.get("locator") or not v.get("original_ingredients"):
                errors.append(f"{rid} 历史配方缺来源/定位/原始用量")
            if profile == "clawhub_mit0" and ("method_original" in v or "method_zh" in v or not v.get("method_summary_zh")):
                errors.append(f"{rid} MIT-0版方法必须是独立中文摘要")
            if v.get("source_id") in src:
                version_source = src[v["source_id"]]
                if version_source.get("kind") == "catalog_only":
                    errors.append(f"{rid} 仅书目不能支撑历史原方")
                if version_source.get("kind") == "secondary" and not v.get("notes"):
                    errors.append(f"{rid} 二手转引配方缺限定说明")
                if version_source.get("kind") in ("primary_transcription", "institutional_excerpt") and v.get("year") != version_source.get("year"):
                    errors.append(f"{rid} 历史版本年份与来源版次不一致")
                if version_source.get("kind") == "secondary" and (not v.get("original_work_title") or not isinstance(v.get("year"), int)):
                    errors.append(f"{rid} 二手转引缺被引原书名/原版年份")
        bridge = r.get("creative_bridge", {})
        for key in ("preserve", "changed_variable", "experiment", "expected_effect", "risk"):
            if not bridge.get(key):
                errors.append(f"{rid} 创作桥接缺 {key}")
        if bridge.get("not_historical") is not True:
            errors.append(f"{rid} 创意未与史实分离")
        if not isinstance(bridge.get("changed_variable"), str):
            errors.append(f"{rid} 变动项不是单个变量字段")
    rec_ids = {r.get("id") for r in records}
    for menu in data.get("menu_frameworks", []):
        for sid in menu.get("record_ids", []):
            if sid not in rec_ids:
                errors.append(f"酒单 {menu.get('id')} 引用不存在的记录 {sid}")
    if data.get("policy", {}).get("earliest_is_scoped") is not True:
        errors.append("缺检索范围限定")
    if data.get("policy", {}).get("historical_sources_do_not_expire") is not True:
        errors.append("历史文献不应按现代酒单月龄过期")
    return errors


def select(data, recipes, query=None, family=None):
    records = data.get("records", [])
    if family:
        fs = {f["id"] for f in data.get("families", []) if norm(family) in (norm(f["id"]), norm(f["name"]))}
        records = [r for r in records if r.get("family_id") in fs]
    if not query:
        return records
    q = norm(query)
    canonical = set()
    for recipe in recipes:
        aliases = [recipe.get("name", ""), recipe.get("name_en", ""), *recipe.get("aliases", [])]
        if q in [norm(x) for x in aliases if x]:
            canonical.add(recipe["name"])
    def terms(record):
        return [norm(x) for x in [record["id"], record["name"], record["name_en"], record.get("canonical_name", ""), *record.get("aliases", [])] if x]
    exact = [r for r in records if q in terms(r) or r.get("canonical_name") in canonical]
    return exact or [r for r in records if any(q in word for word in terms(r))]


def source_ids(records):
    return {sid for r in records for c in r.get("claims", []) for sid in c.get("source_ids", [])} | {v["source_id"] for r in records for v in r.get("historical_versions", [])}


def show_sources(sources):
    for s in sources:
        print(f"[{s['id']}] {s['title']} | {s['author']} | {s['year']} | {s['edition']}")
        print(f"  证据载体：{s['kind']} / {s['verification']}；核查日 {s['accessed']}")
        print(f"  {s['url']}")
        if s.get("note"):
            print(f"  边界：{s['note']}")


def show_record(r, sources, recipes, compare=False, creative=False):
    print(f"\n{r['name']} ({r['name_en']}) | {r['family_id']}")
    print(r["summary"])
    for c in r["claims"]:
        print(f"  [{LABELS[c['status']]}] {c['text']}")
        print(f"    定位：{c['locator']}")
        if c.get("summary"):
            print(f"    独立事实摘要（非原书原文/逐句译文）：{c['summary']}")
        elif c.get("quote_en"):
            print(f"    原文：{c['quote_en']}\n    中文：{c['quote_zh']}")
        for sid in c["source_ids"]:
            s = sources[sid]
            print(f"    出处：{s['title']} ({s['year']}) · {s['edition']} · {s['kind']}/{s['verification']} {s['url']}")
        if c.get("note"):
            print(f"    注意：{c['note']}")
    print(f"  起源边界：{r['origin_caution']}")
    print(f"  结构：{r['structure']}")
    if compare:
        for v in r.get("historical_versions", []):
            s = sources[v["source_id"]]
            provenance = "二手研究转引（未直接核原书）" if s["kind"] == "secondary" else "已读转录/机构摘录（非扫描逐字核对）"
            print(f"  历史版本 {v['year']} · {v['label']} · {v['locator']} · {provenance}")
            print(f"    版本出处：{s['title']} · {s['author']} · {s['edition']} · {s['kind']}/{s['verification']} {s['url']}")
            for ingredient in v["original_ingredients"]:
                print(f"    原始材料记载：{ingredient}")
            if v.get("method_summary_zh"):
                print(f"    方法摘要（独立整理，非原文）：{v['method_summary_zh']}")
            else:
                print(f"    原书操作：{v.get('method_original', '')}")
                print(f"    中文操作：{v.get('method_zh', '')}")
            print(f"    适配边界：{v.get('notes', '')}")
        modern = next((x for x in recipes if x['name'] == r.get('canonical_name')), None)
        if modern:
            print(f"  现代出品库（不是原书换算）：{modern['name']}")
            print("    " + " | ".join(f"{i['name']} {i['amount']}{i['unit']}" for i in modern['ingredients']))
            print(f"    {modern['method']} / {modern['glass']}")
        else:
            print("  本记录未对应现代出品库，不能据旧单位自动生成毫升配方。")
    if creative:
        b = r["creative_bridge"]
        print("  历史启发的现代研发简报（非原方，未经实饮验证）")
        print(f"    不动：{'；'.join(b['preserve'])}")
        print(f"    只动：{b['changed_variable']}")
        print(f"    对照：{b['experiment']}")
        print(f"    预期：{b['expected_effect']}\n    风险：{b['risk']}")
        print("    先做半杯；记录改动/感知/下一轮调整，不宣称一定好喝。")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--sources", action="store_true")
    parser.add_argument("--family")
    parser.add_argument("--compare", action="store_true")
    parser.add_argument("--creative", action="store_true")
    parser.add_argument("--menu", action="store_true")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        data = load(ROOT / "cocktail_history.json")
        recipes = load(ROOT / "recipes.json")["recipes"]
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"历史资料暂不可用：{exc}；不要退回旧故事断言或编造出处。", file=sys.stderr)
        return 2
    if args.validate:
        errors = validate(data, recipes)
        print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2) if args.json else ("历史数据结构校验通过（不等于自动核验史实）" if not errors else "\n".join(errors)))
        return 1 if errors else 0
    errors = validate(data, recipes)
    if errors:
        print("历史证据结构不完整，停止事实输出：" + "；".join(errors[:5]), file=sys.stderr)
        return 2
    records = select(data, recipes, args.query, args.family)
    if args.stats:
        payload = {"version": data.get("version"), "records": len(data["records"]), "sources": len(data["sources"]), "families": len(data["families"]), "claim_statuses": dict(collections.Counter(c["status"] for r in data["records"] for c in r["claims"]))}
    elif args.menu:
        payload = {"menu_frameworks": data.get("menu_frameworks", []), "note": "历史主题是组织方式，不是一次喝完全部的指示；可单杯点选，另设独立无酒精路线。"}
    elif args.sources:
        ids = source_ids(records)
        payload = {"sources": [s for s in data["sources"] if (not args.query and not args.family) or s["id"] in ids]}
    else:
        if not records:
            payload = {"records": [], "note": "未收录/未命中此酒的已核历史；不要宣称查无此酒，不要回退成无出处传说。"}
            print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["note"])
            return 1
        ids = source_ids(records)
        payload = {"records": records, "sources": [s for s in data["sources"] if s["id"] in ids], "policy": data["policy"]}
        if args.compare:
            canonical_names = {r.get("canonical_name") for r in records}
            payload["modern_recipes"] = [r for r in recipes if r["name"] in canonical_names]
            payload["modern_recipe_note"] = "现代出品库，不是原书换算；历史原料保持原单位。"
        if args.creative:
            payload["creative_note"] = "现代研发简报，非原方，未经实饮验证；先半杯单变量对照。"
    if args.json or args.stats:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif args.menu:
        for menu in payload["menu_frameworks"]:
            print(f"\n{menu['name']}\n  排法：{menu['how']}\n  为什么：{menu['why']}\n  示例锚点：{', '.join(menu['record_ids'])}")
        print(payload["note"])
    elif args.sources:
        show_sources(payload["sources"])
    elif args.list:
        for r in records:
            print(f"{r['name']} | {r['name_en']} | {r['family_id']} | {r['summary']}")
    else:
        for r in records:
            show_record(r, {s["id"]: s for s in data["sources"]}, recipes, args.compare, args.creative)
    return 0


if __name__ == "__main__":
    sys.exit(main())
