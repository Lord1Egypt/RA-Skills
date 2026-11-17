#!/usr/bin/env python3
"""promote_draft.py — 提升段：盘点指标 → 可逐条审阅的结构化草稿（ai-data-delivery v0.0.9）

harvest_metrics.py 解决了"把既有指标库盘点成清单"，本工具解决最后一公里：
把清单逐条翻译成接近可合入 semantic.yaml 的结构化草稿，人工审阅后用
patch_model.py batch 一次合入——不再手写翻译脚本。

四分输出（沿用真实项目验证过的分类法）：
  ✅ 可直接合入：count 型 + 字段/值全部对上宽表枚举 → ops.yaml（可直接 batch）
  🔶 映射待确认：字段/值有提议映射但需人审（cn 推断、枚举近似、非 COUNT 聚合）
                 → ops_review.yaml（确认后 batch）+ 提升清单.md
  ⛔ 需业务定义：派生引用（公式里引用其他指标）或宽表无对应字段 → 只进清单
  📋 明细模板：list/rank 类不进 metrics，产出 templates 段草稿（明细查询是一等资产）

用法：
  python promote_draft.py --raw inventory/metrics_raw.yaml --from-meta meta/ \
      --model semantic.yaml --out promote/
  python promote_draft.py --raw metrics_raw.yaml --from-meta meta/ --model semantic.yaml \
      --syn-map 同义词补充.yaml --out promote/     # 可选：{指标id: [词...]} 领域同义词素材

输入约定：
  --raw       harvest_metrics.py 产出（metrics: id/name/type/source_table/mapped_table/
              formula_raw/status/rule_bound）；type ∈ num|pct|list|rank
  --from-meta gen_metadata.py 产出并人审后的 meta 目录（table + columns{name,cn,enum}）
  --model     当前 semantic.yaml（跳过已合入指标、解析数据集与时间字段）

时间字段缺省：数据集有 stat_date 用 stat_date，否则取第一个 role=time 字段（快照宽表惯例）。

边界：本工具只做字段/枚举的机械翻译与分类提议，不发明口径；🔶/⛔ 必须人审，
✅ 合入后仍须 patch_model struct --db 验算 + run_eval 金标准回归才算发布。
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

from _contract import load

COND_RE = re.compile(r"([一-鿿A-Za-z_][\w一-鿿]*)\s*(<>|>=|<=|=|>|<)\s*(?:'([^']*)'|(\d+(?:\.\d+)?))")
DERIVED_RE = re.compile(r"[一-鿿]+(?:数|率)(?![\w'])")
NAME_SUFFIX = re.compile(r"(数|总数|数量|明细|统计|情况|排行|提醒|报告|率)$")
PROFILE_TABLE = re.compile(r"profile|画像|snapshot|档案")


def load_meta_index(meta_dir):
    """meta/*.yaml → {table: {col: {cn, enum[]}}}。enum 兼容 dict（键为取值）与 list。"""
    idx = {}
    for p in sorted(Path(meta_dir).glob("*.yaml")):
        meta = load(str(p)) or {}
        table = meta.get("table") or p.stem
        cols = {}
        for c in meta.get("columns") or []:
            enum = c.get("enum")
            enum_vals = [str(k) for k in enum] if isinstance(enum, dict) else \
                [str(v) for v in (enum or [])]
            cols[c["name"]] = {"cn": c.get("cn", ""), "enum": enum_vals}
        idx[table] = cols
    return idx


def pick_time(ds):
    tfs = [f["name"] for f in ds.get("fields", []) if f.get("role") == "time"]
    return "stat_date" if "stat_date" in tfs else (tfs[0] if tfs else None)


def translate_where(where, cols):
    """WHERE 伪代码 → extra_where 片段。返回 (片段, 问题清单)。
    字段三级解析：物理名直中 → cn 全等（唯一）→ cn 近似包含（唯一，标【推断字段】）。"""
    issues, parts = [], []
    for m in COND_RE.finditer(where or ""):
        field, op, sval, nval = m.group(1), m.group(2), m.group(3), m.group(4)
        val = sval if sval is not None else nval
        phys = None
        if field in cols:
            phys = field
        else:
            cand = [n for n, c in cols.items() if c["cn"] == field]
            if len(cand) == 1:
                phys = cand[0]
            elif len(cand) > 1:
                issues.append(f"字段「{field}」cn 多义：{cand}")
            else:
                near = [n for n, c in cols.items()
                        if c["cn"] and (field in c["cn"] or (c["cn"] in field and len(c["cn"]) >= 2))]
                if len(near) == 1:
                    issues.append(f"【推断字段】「{field}」按 cn 近似 → {near[0]}（{cols[near[0]]['cn']}），需人审")
                    phys = near[0]
                elif near:
                    issues.append(f"字段「{field}」近似多义：{[(n, cols[n]['cn']) for n in near]}")
        if not phys:
            issues.append(f"【字段缺口】宽表无「{field}」对应列")
            continue
        lit = f"'{val}'" if sval is not None else val
        if sval is not None:
            enum = cols[phys]["enum"]
            if enum and val not in enum:
                near = [e for e in enum if val in e or e in val]
                if len(near) == 1:
                    issues.append(f"【值待确认】{phys} 枚举无 '{val}'，提议 → '{near[0]}'（枚举：{enum}）")
                    lit = f"'{near[0]}'"
                else:
                    issues.append(f"【值待确认】{phys} 枚举无 '{val}'，无近似（枚举：{enum}）")
                    continue
        parts.append(f"{phys} {op} {lit}")
    return " AND ".join(parts), issues


def synonyms_for(mid, name, syn_map):
    """通用同义词生成：原称 + 去后缀词根 + 问法形态；--syn-map 可叠加领域素材。"""
    syn = list((syn_map or {}).get(mid, []))
    if name and name not in syn:
        syn.insert(0, name)
    root = NAME_SUFFIX.sub("", name or "")
    if root and root != name and root not in syn and len(root) >= 2:
        syn.append(root)
    if name:
        q = f"多少{name}" if len(name) <= 4 else f"{name}有多少"
        if q not in syn:
            syn.append(q)
    return syn[:6]


def classify(x, ctx):
    """单条盘点指标 → 草稿条目。ctx: src2ds / ds_time / meta_idx / syn_map / promoted。"""
    mid, name = x.get("id"), x.get("name")
    table = x.get("mapped_table")
    ds = ctx["src2ds"].get(table)
    cols = ctx["meta_idx"].get(table, {})
    formula = x.get("formula_raw") or ""
    mwhere = re.search(r"\bWHERE\b(.+?)(?:ORDER\s+BY|$)", formula, re.I | re.S)
    where = mwhere.group(1).strip() if mwhere else ""
    extra, issues = translate_where(where, cols)

    entry = {"id": mid, "name": name, "dataset": ds, "wide_table": table,
             "synonyms": synonyms_for(mid, name, ctx["syn_map"]),
             "formula_raw": formula, "source_table": x.get("source_table"),
             "rule_bound": bool(x.get("rule_bound")),
             "extra_where": extra or None, "issues": issues}
    if ds is None:
        entry["issues"] = [f"【模型缺口】映射宽表 {table} 不在 semantic.yaml datasets 中，"
                           "需先把该表建模为数据集"] + entry["issues"]

    if x.get("type") in ("list", "rank"):
        entry["kind"] = "📋 明细模板"
        sel = re.search(r"SELECT\s+(.+?)\s+FROM", formula, re.I | re.S)
        entry["select_raw"] = sel.group(1).strip() if sel else ""
        entry["time_field"] = ctx["ds_time"].get(ds)
        if table and PROFILE_TABLE.search(table):
            entry["issues"] = [f"【粒度存疑】{table} 疑似主体快照粒度，明细行可能装不下，"
                               "需核对宽表 grain 或改用明细宽表"] + entry["issues"]
        return "templates", entry

    is_count = re.match(r"\s*SELECT\s+COUNT\s*\(\s*\*\s*\)", formula, re.I)
    is_ratio = x.get("type") == "pct" or "/" in formula
    derived = [d for d in DERIVED_RE.findall(formula) if d != name]

    if derived and not is_count:
        entry.update(kind="⛔ 需业务定义",
                     reason=f"口径引用派生指标 {derived}，需业务给出宽表字段级定义")
    elif is_count:
        entry.update(kind="✅ 可直接合入" if not issues else "🔶 映射待确认",
                     type="count", expr="COUNT(*)",
                     time_field=ctx["ds_time"].get(ds))
    elif is_ratio:
        entry.update(kind="⛔ 需业务定义" if derived else "🔶 映射待确认",
                     type="ratio",
                     reason="比率型需拆分子/分母（禁行级平均）"
                            + (f"；派生引用 {derived}" if derived else ""))
    else:
        entry.update(kind="🔶 映射待确认", type="count", expr="COUNT(*)",
                     time_field=ctx["ds_time"].get(ds),
                     reason="SELECT 非 COUNT(*)，按 count 草拟，需确认聚合语义")
    if entry["kind"].startswith("✅") and ds is None:
        entry["kind"] = "🔶 映射待确认"  # 模型缺口未补不能算可直接合入
    return "drafts", entry


def to_struct_op(d):
    """✅/🔶 草稿 → patch_model batch struct op。"""
    op = {"op": "struct", "id": d["id"], "create": True, "name": d.get("name"),
          "type": d.get("type", "count"), "dataset": d.get("dataset"),
          "expr": d.get("expr", "COUNT(*)")}
    if d.get("extra_where"):
        op["extra_where"] = d["extra_where"]
    if d.get("time_field"):
        op["time_field"] = d["time_field"]
    if d.get("synonyms"):
        op["synonyms"] = d["synonyms"]
    return op


def to_template(d):
    """📋 明细模板草稿 → semantic.yaml templates 段条目。"""
    cols = [c.strip() for c in (d.get("select_raw") or "").split(",") if c.strip()]
    return {"id": d["id"], "name": d.get("name"), "dataset": d.get("dataset"),
            "columns_raw": cols or None, "extra_where": d.get("extra_where"),
            "time_field": d.get("time_field"), "synonyms": d.get("synonyms"),
            "status": "草案",
            "note": "columns_raw 是伪代码 SELECT 列原文，需人审映射为数据集物理列"}


def render_checklist(summary, drafts, templates, model_path, raw_path, unmapped=None):
    L = ["# 指标提升审阅清单", "",
         f"- 盘点来源：`{raw_path}`；目标模型：`{model_path}`",
         f"- 分类：✅ 可直接合入 {summary['✅ 可直接合入']} 条 / "
         f"🔶 映射待确认 {summary['🔶 映射待确认']} 条 / "
         f"⛔ 需业务定义 {summary['⛔ 需业务定义']} 条 / 📋 明细模板 {summary['📋 明细模板']} 条 / "
         f"⚠️ 表名未映射 {summary.get('⚠️ 表名未映射', 0)} 条",
         "",
         "操作路径：✅ 已在 `ops.yaml`（核对后 `patch_model.py -f 模型 batch ops.yaml --db 库`）；",
         "🔶 在 `ops_review.yaml`，逐条确认提议映射后同法合入；⛔ 找业务补字段级口径；",
         "📋 在 `templates_draft.yaml`，人审列映射后并入 semantic.yaml `templates:` 段；",
         "⚠️ 先补 harvest 的表名映射（--mapping 或 meta sources）再重跑。", ""]
    if unmapped:
        L.append("## ⚠️ 表名未映射（有来源表但映射不到宽表，先补映射）")
        L.append("")
        for x in unmapped:
            L.append(f"- {x.get('id')} {x.get('name') or ''}：来源表 `{x.get('source_table')}` 未映射")
        L.append("")
    for tag, pred in (("⛔ 需业务定义（找业务补口径）", lambda d: d["kind"].startswith("⛔")),
                      ("🔶 映射待确认（人审提议）", lambda d: d["kind"].startswith("🔶")),
                      ("✅ 可直接合入（已进 ops.yaml）", lambda d: d["kind"].startswith("✅"))):
        L.append(f"## {tag}")
        L.append("")
        for d in [d for d in drafts if pred(d)]:
            L.append(f"### {d['id']} {d.get('name') or ''}")
            L.append(f"- 宽表：{d.get('wide_table')} → 数据集：{d.get('dataset')}")
            if d.get("reason"):
                L.append(f"- 原因：{d['reason']}")
            for iss in d.get("issues") or []:
                L.append(f"- {iss}")
            if d.get("extra_where"):
                L.append(f"- 提议 extra_where：`{d['extra_where']}`")
            L.append(f"- 原始口径：`{(d.get('formula_raw') or '').strip()}`")
            L.append("")
    if templates:
        L.append("## 📋 明细模板（进 templates 段，不进 metrics）")
        L.append("")
        for d in templates:
            L.append(f"### {d['id']} {d.get('name') or ''}")
            L.append(f"- 宽表：{d.get('wide_table')} → 数据集：{d.get('dataset')}；"
                     f"时间字段：{d.get('time_field')}")
            for iss in d.get("issues") or []:
                L.append(f"- {iss}")
            L.append(f"- 原始 SELECT 列：`{d.get('select_raw')}`")
            L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="盘点指标 → 可审阅的结构化提升草稿（v0.0.9）")
    ap.add_argument("--raw", required=True, help="harvest_metrics.py 产出的 metrics_raw.yaml")
    ap.add_argument("--from-meta", required=True, help="meta 目录（gen_metadata 产出并人审）")
    ap.add_argument("--model", required=True, help="当前 semantic.yaml")
    ap.add_argument("--syn-map", default=None, help="可选 {指标id: [同义词...]} 领域素材")
    ap.add_argument("--out", default="promote", help="输出目录（默认 promote/）")
    args = ap.parse_args()

    raw_doc = load(args.raw) or {}
    raw = raw_doc.get("metrics") or []
    if not raw:
        print(f"错误：{args.raw} 无 metrics 条目", file=sys.stderr)
        return 2
    model = load(args.model) or {}
    syn_map = load(args.syn_map) if args.syn_map else {}
    ctx = {
        "promoted": {mt.get("id") for mt in model.get("metrics", []) or []},
        "src2ds": {ds.get("source"): ds.get("name") for ds in model.get("datasets", []) or []},
        "ds_time": {ds.get("name"): pick_time(ds) for ds in model.get("datasets", []) or []},
        "meta_idx": load_meta_index(args.from_meta),
        "syn_map": syn_map if isinstance(syn_map, dict) else {},
    }

    drafts, templates, skipped, unmapped = [], [], [], []
    for x in raw:
        if not x.get("mapped_table"):
            if x.get("source_table") and x.get("source_table") != "—NO_TABLE—":
                unmapped.append(x)  # 有来源表但没映射到宽表：映射缺口，必须可见
            else:
                skipped.append((x.get("id"), "无来源表（已在 gaps.yaml 登记）"))
            continue
        if x.get("id") in ctx["promoted"]:
            skipped.append((x.get("id"), "已在模型 metrics 中"))
            continue
        bucket, entry = classify(x, ctx)
        (templates if bucket == "templates" else drafts).append(entry)

    summary = {"✅ 可直接合入": sum(1 for d in drafts if d["kind"].startswith("✅")),
               "🔶 映射待确认": sum(1 for d in drafts if d["kind"].startswith("🔶")),
               "⛔ 需业务定义": sum(1 for d in drafts if d["kind"].startswith("⛔")),
               "📋 明细模板": len(templates),
               "⚠️ 表名未映射": len(unmapped), "跳过": len(skipped)}

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = {"source": {"raw": args.raw, "model": args.model, "meta": args.from_meta},
           "summary": summary, "drafts": drafts, "detail_templates": templates,
           "unmapped": [{"id": x.get("id"), "name": x.get("name"),
                         "source_table": x.get("source_table")} for x in unmapped],
           "skipped": [{"id": i, "reason": r} for i, r in skipped]}
    (out_dir / "promote_draft.yaml").write_text(
        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    ops = [to_struct_op(d) for d in drafts if d["kind"].startswith("✅")]
    ops_review = [to_struct_op(d) for d in drafts if d["kind"].startswith("🔶")]
    (out_dir / "ops.yaml").write_text(
        yaml.safe_dump({"ops": ops}, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8")
    (out_dir / "ops_review.yaml").write_text(
        yaml.safe_dump({"ops": ops_review}, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8")
    (out_dir / "templates_draft.yaml").write_text(
        yaml.safe_dump({"templates": [to_template(d) for d in templates]},
                       allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    (out_dir / "提升清单.md").write_text(
        render_checklist(summary, drafts, templates, args.model, args.raw,
                         unmapped=unmapped), encoding="utf-8")

    print(f"草稿 {len(drafts)} 条 + 明细模板 {len(templates)} 条"
          f"（未映射 {len(unmapped)} / 跳过 {len(skipped)}）→ {out_dir}/")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print("产出：promote_draft.yaml / ops.yaml(✅) / ops_review.yaml(🔶) / "
          "templates_draft.yaml(📋) / 提升清单.md")
    print("下一步：审 提升清单.md → patch_model.py batch ops.yaml --db 物理库 验算合入 → "
          "run_eval 金标准回归")
    return 0


if __name__ == "__main__":
    sys.exit(main())
