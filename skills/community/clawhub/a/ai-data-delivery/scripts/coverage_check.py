#!/usr/bin/env python3
"""coverage_check.py — 建模段门禁：覆盖率校验（ai-data-delivery v0.0.4）

指标 ↔ 模型 ↔ gold 三方覆盖矩阵。门禁规则：存在"未进模型且未登记缺口"的孤儿指标 → 失败。

用法：
  python coverage_check.py --model semantic.yaml [--metrics-raw inventory/metrics_raw.yaml] \
      [--gaps inventory/gaps.yaml] [--cases cases_gold.json] [--out coverage.md]

检查：
  1. 指标覆盖：metrics_raw 每条 → 模型里有没有（按 id）→ structured 与否
  2. 孤儿指标：不在模型且不在 gaps.yaml 登记 → ERROR
  3. gold 覆盖：每条用例的 expect_table 有数据集认领；问句至少命中一个指标同义词/概念/数据集同义词
  4. 数据集使用度：未被任何指标使用的数据集（INFO）
退出码：0=无 ERROR；1=有 ERROR。
"""
import os
import argparse
import json
import re
import sys

import yaml
from _contract import load


def load_cases(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f) if path.endswith(".json") else yaml.safe_load(f)
    if isinstance(data, dict):
        for k in ("cases", "gold_results"):
            if k in data:
                return data[k]
    return data


def main():
    ap = argparse.ArgumentParser(description="指标↔模型↔gold 覆盖率校验")
    ap.add_argument("--model", required=True)
    ap.add_argument("--metrics-raw", default=None)
    ap.add_argument("--gaps", default=None)
    ap.add_argument("--cases", default=None)
    ap.add_argument("--out", default=None, help="覆盖矩阵报告（md）")
    args = ap.parse_args()

    m = load(args.model)
    model_metric_ids = {x.get("id") for x in m.get("metrics", [])}
    structured_ids = {x.get("id") for x in m.get("metrics", []) if x.get("structured")}
    ds_names = {d.get("name") for d in m.get("datasets", [])}
    ds_sources = {d.get("source") for d in m.get("datasets", [])}

    errors, warns, infos, lines = [], [], [], []

    # 1/2. 指标覆盖
    if args.metrics_raw:
        raw = load(args.metrics_raw)["metrics"]
        gap_ids = set()
        if args.gaps:
            gap_ids = {g["metric_id"] for g in
                       load(args.gaps)["gaps"]}
        n_in = n_struct = 0
        for r in raw:
            rid = r.get("id")
            if rid in model_metric_ids:
                n_in += 1
                if rid in structured_ids:
                    n_struct += 1
                else:
                    warns.append(f"指标 {rid}（{r.get('name')}）在模型但未结构化——暂不落地需显式声明")
            elif rid in gap_ids:
                infos.append(f"指标 {rid}（{r.get('name')}）已登记数据缺口")
            else:
                errors.append(f"孤儿指标：{rid}（{r.get('name')}）不在模型也未登记缺口")
        lines.append(f"## 指标覆盖\n\n- 指标库总数：{len(raw)}；进模型：{n_in}；已结构化：{n_struct}\n"
                     f"- 已登记缺口：{len(gap_ids & {r.get('id') for r in raw})}；孤儿：{sum(1 for e in errors if e.startswith('孤儿'))}\n")

    # 3. gold 覆盖
    if args.cases:
        cases = load_cases(args.cases)
        vocab = set(ds_names) | set(ds_sources)
        for x in m.get("metrics", []):
            vocab.add(x.get("name", ""))
            vocab.update(x.get("synonyms", []) or [])
        for c in m.get("concepts", []):
            vocab.add(c.get("term", ""))
            vocab.update(c.get("aliases", []) or [])
        for d in m.get("datasets", []):
            vocab.update((d.get("ai") or {}).get("synonyms", []) or [])
        uncovered = []
        for c in cases:
            et = c.get("expect_table")
            if et and not re.search(r"拒绝|追问|无表|澄清", str(et)):
                for t in re.split(r"[|,，]", str(et)):
                    t = t.strip()
                    if t and t not in ds_sources:
                        errors.append(f"用例 {c.get('id')} 的 expect_table {t!r} 无数据集认领")
            if c.get("expect_reject") or (c.get("expect") or {}).get("type") == "refusal":
                continue  # Refusal cases probe the guard boundary, not term-vocabulary coverage.
            q = c.get("question", "")
            if q and not any(v and v in q for v in vocab):
                uncovered.append(c.get("id"))
        if uncovered:
            warns.append(f"问句未命中任何已知词表（同义词/概念/表别名）的用例 {len(uncovered)} 条："
                         f"{uncovered[:10]}——试点期大概率不识别，先补同义词")
        lines.append(f"## gold 覆盖\n\n- 用例 {len(cases)} 条；词表未命中 {len(uncovered)} 条\n")

    # 4. 数据集使用度
    used = {x.get("dataset") for x in m.get("metrics", []) if x.get("dataset")}
    for d in sorted(ds_names - used):
        infos.append(f"数据集 {d} 未被任何指标挂载（仅 NL2SQL 兜底使用，确认是否有意为之）")

    for e in errors:
        print(f"[ERROR] {e}")
    for w in warns[:20]:
        print(f"[WARN ] {w}")
    for i in infos[:20]:
        print(f"[INFO ] {i}")
    print(f"\n覆盖率校验：{len(errors)} ERROR / {len(warns)} WARN / {len(infos)} INFO")

    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write("# 覆盖率校验报告\n\n" + "\n".join(lines)
                    + "\n## 明细\n\n"
                    + "".join(f"- ERROR {e}\n" for e in errors)
                    + "".join(f"- WARN {w}\n" for w in warns)
                    + "".join(f"- INFO {i}\n" for i in infos))
        print(f"报告 → {args.out}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
