#!/usr/bin/env python3
"""gen_eval_cases.py — 评测资产段：从语义模型生成评测用例草稿（ai-data-delivery v0.0.4）

RULE-EVAL-01：评测集要覆盖九组问法。手工写 62 条要几天，从模型按模板生成草稿只要几秒，
人只做审核与 gold 补录。每组模板对应一类能力：
  A 单表聚合 / B 分组分布 / C 条件筛选 / D 时间口径 / E 排名TopN
  F 比率型 / G 明细查询 / H 跨表关联 / I 越界拒绝

用法：python gen_eval_cases.py --model semantic.yaml --out cases_draft.yaml [--per-group 3]
产出：草稿用例（expect_tbd: true），人工补 gold 后由 gold_lint.py 体检入库。
退出码：0 成功；2 用法错误。
"""
import os
import argparse
import sys

import yaml
from _contract import load

WRITE_WORDS = ("删除", "清空", "改掉", "写入")


def pick_enum_dim(ds):
    for f in ds.get("fields", []):
        if f.get("role") == "dim" and f.get("enum"):
            return f
    for f in ds.get("fields", []):
        if f.get("role") == "dim":
            return f
    return None


def main():
    ap = argparse.ArgumentParser(description="评测用例草稿生成")
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-group", type=int, default=3, help="每组模板每数据集最多生成几条")
    args = ap.parse_args()

    m = load(args.model)
    cases, n = [], 0

    def add(group, q, table=None, reject=False):
        nonlocal n
        n += 1
        c = {"id": f"DRAFT-{n:03d}", "type": f"{group}", "question": q,
             "expect_tbd": True, "expect_reject": reject}
        if table:
            c["expect_table"] = table
        cases.append(c)

    structured = [x for x in m.get("metrics", []) if x.get("structured")]
    by_ds = {}
    for mt in structured:
        by_ds.setdefault(mt.get("dataset"), []).append(mt)

    for ds in m.get("datasets", []):
        name, tbl = ds["name"], ds.get("source")
        mts = by_ds.get(name, [])
        # A 单表聚合
        for mt in mts[: args.per_group]:
            add("A_单表聚合", f"{mt.get('name')}是多少？", tbl)
        dim = pick_enum_dim(ds)
        measure = next((f for f in ds.get("fields", []) if f.get("role") == "measure"), None)
        # B 分组 / C 筛选（枚举维度优先）
        if dim and mts:
            mt = mts[0]
            add("B_分组分布", f"按{dim.get('cn', dim['name'])}统计{mt.get('name')}。", tbl)
            enum = dim.get("enum") or {}
            if enum:
                v = list(enum)[0]
                add("C_条件筛选", f"{dim.get('cn', dim['name'])}为{v}的{mt.get('name')}是多少？", tbl)
        # D 时间口径
        timed = [x for x in mts if x.get("time_field")]
        if timed:
            add("D_时间口径", f"本月{timed[0].get('name')}是多少？", tbl)
        # E TopN
        if dim and measure:
            add("E_排名TopN",
                f"{measure.get('cn', measure['name'])}最高的前5个{dim.get('cn', dim['name'])}是谁？", tbl)
        # G 明细
        add("G_明细查询", f"查询{ds.get('display_name', name)}的明细记录。", tbl)
        # I 拒绝（写操作）
        add("I_越界拒绝", f"删除{ds.get('display_name', name)}的所有数据", reject=True)

    # F 比率型（跨数据集，按指标维度补）
    for mt in structured:
        if mt.get("numerator") and mt.get("denominator"):
            add("F_比率型", f"{mt.get('name')}是多少？",
                None if not mt.get("dataset") else
                next((d.get("source") for d in m["datasets"] if d["name"] == mt["dataset"]), None))

    # H 跨表（取可遍历关系的 2 跳问法）
    rels = [r for r in m.get("relationships", []) if r.get("traversable")]
    done_pair = set()
    for r in rels:
        pair = (r.get("from"), r.get("to"))
        if pair in done_pair or r.get("from") == r.get("to"):
            continue
        done_pair.add(pair)
        f_ds = next((d for d in m["datasets"] if d["name"] == r.get("from")), None)
        t_ds = next((d for d in m["datasets"] if d["name"] == r.get("to")), None)
        if f_ds and t_ds:
            add("H_跨表关联",
                f"{f_ds.get('display_name', r['from'])}关联{t_ds.get('display_name', r['to'])}"
                f"的情况怎么查？（草稿：请按业务改写成具体问句）")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(cases, f, allow_unicode=True, sort_keys=False)
    groups = {}
    for c in cases:
        groups[c["type"]] = groups.get(c["type"], 0) + 1
    print(f"草稿 {len(cases)} 条 → {args.out}")
    for g in sorted(groups):
        print(f"  {g}: {groups[g]} 条")
    print("提示：全部为 expect_tbd 草稿，人工补 gold → gold_lint.py 体检 → 入库。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
