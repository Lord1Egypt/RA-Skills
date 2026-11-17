#!/usr/bin/env python3
"""
DND Lens · 联动流水线（一站式）

把三大子技能串成一条线：
  真实经历 / 已有草稿
    → echo-map   （脱敏 + 按 mapping_dict 规则映射为 DND 草稿 + 补全契约）
    → module-forge（注入草稿，叠加 DMG 标准 CR 平衡与分幕）
    → world-lore （按设定/地点/派系检索背景知识卡，填充锚点）

用法：
  # 方式 A：给一段真实经历，自动生成并平衡
  python lens_pipeline.py --story 经历.txt --names "张三 李四" --places "上海 甲公司" \
       --players 4 --level 5 --duration medium --type 都市寻宝 \
       --setting "被遗忘的国度/深水城" --tone 悬疑 --out 产出.json

  # 方式 B：已有 LLM 起草的草稿，仅做过平衡 + 背景检索
  python lens_pipeline.py --inject-draft 草稿.json --names "张三" --places "上海" \
       --players 3 --level 3 --duration short --type 地城探险 --setting 费伦

注意：隐私优先。若未提供 --names/--places，脚本不会对真实身份做猜测性替换，
      仅在报告中提示「未脱敏」。
"""

import argparse
import importlib.util
import json
import sys
import types
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent          # .../dnd-dm-skill
sys.path.insert(0, str(SKILL / "scripts"))

import lens_rag


def _load_module_forge():
    spec = importlib.util.spec_from_file_location(
        "module_forge_mod", SKILL / "module-forge" / "scripts" / "module_forge.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


module_forge = _load_module_forge()


def _load_echo():
    spec = importlib.util.spec_from_file_location(
        "echo_map_mod", SKILL / "echo-map" / "scripts" / "echo_map.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_rule_draft(story_text, names, places, echo, mdict, args):
    """无 LLM 时的规则映射：脱敏名 → NPC/地点/派系，故事 → premise。"""
    alias = echo.build_alias_map(names, places, mdict)
    anon = echo.apply_alias(story_text, alias)

    person = mdict["slots"]["person"]
    role_presets = person["role_presets"]            # dict: 类别 -> {class/race, note}
    role_keys = list(role_presets.keys())
    person_align = person["candidates"]["alignment"]  # 完整阵营列表

    auth = mdict["slots"]["authority"]["candidates"]
    auth_class = auth.get("class", ["术士"])[0]
    auth_align = auth.get("alignment", ["守序邪恶"])[0]
    auth_faction = auth.get("faction", ["秘密结社"])[0]

    loc_nodes = mdict["slots"]["location"]["candidates"].get("location_node", [])
    villain = mdict["slots"]["conflict"]["candidates"].get("villain_archetype", ["野心贵族"])[0]

    # NPC：每个真实名轮转映射到一个角色原型类别，取 class/race + 阵营
    npcs = []
    for i, real in enumerate(names):
        fan = alias.get(real, real)
        cat = role_keys[i % len(role_keys)]
        preset = role_presets[cat]
        npcs.append({
            "name": fan,
            "role": cat,
            "class": preset.get("class", preset.get("race", "")),
            "alignment": person_align[i % len(person_align)],
        })

    # 地点节点映射
    locs = []
    for i, real in enumerate(places):
        fan = alias.get(real, real)
        node = loc_nodes[i % len(loc_nodes)] if loc_nodes else fan
        locs.append({"node": fan, "maps_to": node})

    # 冲突 → 反派 archetype + 权力者阵营
    factions = [{"name": f"{villain}（暗影）", "alignment": auth_align,
                 "class_hint": auth_class, "faction_hint": auth_faction}]

    return {
        "title": f"《{args.setting}·一段来自尘世的回响》",
        "premise": anon,
        "npcs": npcs,
        "factions": factions,
        "locations": locs,
        "level_range": f"{args.level}-{args.level}",
        "type": args.type or "都市奇幻",
        "timeline": "（据经历跨度，DM 酌定）",
    }, alias, anon


def main():
    p = argparse.ArgumentParser(description="DND Lens 联动流水线（经历→映射→平衡→背景）")
    p.add_argument("--story", help="真实经历文本文件（方式 A）")
    p.add_argument("--inject-draft", help="已有草稿 JSON（方式 B，跳过规则映射）")
    p.add_argument("--names", nargs="*", default=[], help="需脱敏的真实人名（空格分隔，中文可整串）")
    p.add_argument("--places", nargs="*", default=[], help="需脱敏的真实地名/机构名")
    p.add_argument("--players", type=int, required=True, help="玩家人数")
    p.add_argument("--level", type=int, required=True, help="队伍等级")
    p.add_argument("--duration", choices=["short", "medium", "long"], required=True, help="时长档")
    p.add_argument("--type", default="", help="冒险类型")
    p.add_argument("--setting", default="被遗忘的国度/费伦", help="设定")
    p.add_argument("--tone", default="", help="基调")
    p.add_argument("--out", help="输出汇总 JSON（默认打印屏幕）")
    args = p.parse_args()

    echo = _load_echo()
    mdict = echo.load_dict()
    names = echo.flat(args.names)
    places = echo.flat(args.places)

    # ---- 步骤 1：echo-map 脱敏 + 映射 ----
    if args.inject_draft:
        draft = json.loads(Path(args.inject_draft).read_text(encoding="utf-8"))
        alias = echo.build_alias_map(names, places, mdict)
        anon = echo.apply_alias(draft.get("premise", ""), alias)
        draft["premise"] = anon
    else:
        if not args.story:
            p.error("方式 A 需提供 --story；或用 --inject-draft 传入已有草稿")
        story_text = Path(args.story).read_text(encoding="utf-8")
        draft, alias, anon = build_rule_draft(story_text, names, places, echo, mdict, args)

    # 补全 echo-map 输出契约（chronicle_note + _meta）
    draft.setdefault("chronicle_note", "（请补一段『这段经历在费伦编年史中可记为何事』的注记）")
    draft["_meta"] = {
        "generated_by": "lens-pipeline",
        "mapping_dict_version": mdict.get("version"),
        "anonymized": bool(alias),
        "alias": alias,
        "privacy_note": mdict["anonymize"]["rule"],
    }
    # 若真实名仍以裸串出现在草稿，再脱敏一遍
    def scrub(obj):
        if isinstance(obj, str):
            return echo.apply_alias(obj, alias)
        if isinstance(obj, list):
            return [scrub(x) for x in obj]
        if isinstance(obj, dict):
            return {k: scrub(v) for k, v in obj.items()}
        return obj
    draft = scrub(draft)

    # ---- 步骤 2：module-forge 注入草稿 + CR 平衡 ----
    draft_path = SKILL / "data" / "_pipeline_draft_tmp.json"
    draft_path.write_text(json.dumps(draft, ensure_ascii=False), encoding="utf-8")
    fa = types.SimpleNamespace(
        players=args.players, level=args.level, duration=args.duration,
        type=args.type or "", setting=args.setting, tone=args.tone or "",
        anchor="", draft=str(draft_path))
    module = module_forge.build_module(fa)

    # ---- 步骤 3：world-lore 检索背景 ----
    lens = lens_rag.WorldLens()
    queries = [args.setting]
    queries += [loc.get("node", "") for loc in draft.get("locations", [])]
    queries += [f.get("name", "") for f in draft.get("factions", [])]
    seen, uniq = set(), []
    for q in queries:
        if not q:
            continue
        for c in lens.search(q, top_k=3, types=["location", "faction", "monster", "event"]):
            if c["id"] not in seen:
                seen.add(c["id"]); uniq.append(c)
    module["world_lore_pack"] = lens.render(uniq[:8], with_body=False)
    module["anchors"] = module.get("anchors") or [
        {"title": c["title"], "type": c["type"], "source": c["source_file"]} for c in uniq[:5]]

    # 清理临时草稿
    try:
        draft_path.unlink()
    except Exception:
        pass

    result = {"echo_map": {"alias": alias, "anonymized": bool(alias),
                           "anonymized_story": anon if not args.inject_draft else "(见草稿)"},
              "module": module}

    out_text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"已写入汇总 JSON：{args.out}")
    else:
        print(out_text)

    # 可读报告
    if not args.out:
        return
    m = module
    print("\n================ 联动流水线 · 可读报告 ================")
    print("标题      :", m["title"])
    print("前提      :", (m.get("premise", "") or "")[:80])
    print("NPC       :", ", ".join(f"{n['name']}({n.get('class','')}/{n.get('alignment','')})" for n in m.get("npcs", [])))
    print("派系      :", ", ".join(f"{f['name']}" for f in m.get("factions", [])))
    print("地点      :", ", ".join(l.get("node", "") for l in m.get("locations", [])))
    print("CR 预算/场:", m["party_cr_budget_per_encounter"])
    print("分幕遭遇  :")
    for a in m["acts"]:
        e = a["encounter"]; s = e.get("suggested") or {}
        print(f"   第{a['act']}幕 {e['difficulty_cn']} | CR {s.get('cr')} | {s.get('count')}x {s.get('monsters')} | XP {s.get('xp_total')}")
    print("背景素材  :", len(uniq), "张知识卡注入")


if __name__ == "__main__":
    main()
