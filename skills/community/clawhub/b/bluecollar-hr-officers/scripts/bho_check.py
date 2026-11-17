#!/usr/bin/env python3
"""BHO 技能结构自检（仅标准库）

用法：python bho_check.py [技能根目录]
默认根目录为脚本上一级。检查项：三层结构、125 单元与依赖、入口占比、身份唯一性、
五槽位、执行框架接口、范本 7 要素与覆盖矩阵、跨文件名称一致性、样例企业圣经一致性。
"""
import re
import sys
from pathlib import Path

DOMAINS = ["X0", "N1", "N2", "N3", "N4", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"]
SLOTS = ["必选组件", "可选组件", "组装顺序", "约束", "格式"]
SECTIONS = ["场景", "输入", "要求覆盖矩阵", "交付物本体", "勾稽", "口径引用"]
ID_RE = re.compile(r"^\|\s*((?:X0|N[1-4]|B(?:10|[1-9]))-\d{2})\s*\|")
ID_ANY = re.compile(r"(?:X0|N[1-4]|B(?:10|[1-9]))-\d{2}")


def read(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    refs = root / "references"
    oks, warns, fails = [], [], []

    skill = read(root / "SKILL.md")
    catalog = read(refs / "BHO-catalog.md")
    reqs = read(refs / "BHO-requirements.md")
    exem = read(refs / "BHO-exemplars.md")

    if not skill:
        fails.append("SKILL.md 缺失")
    if "定位" in skill and ("依赖声明" in skill or "派生自" in skill):
        oks.append("A2 定位与依赖声明")
    else:
        fails.append("A2 缺定位或依赖声明")
    if "使用规则" in skill and "降级" in skill:
        oks.append("A3/A4 使用规则与降级模式")
    else:
        fails.append("A3/A4 使用规则或降级模式缺失")
    if "域间逻辑流" in catalog.split("\n## ")[0]:
        oks.append("A5 catalog 头部域间逻辑流")
    else:
        fails.append("A5 catalog 头部缺域间逻辑流")
    if "依赖拓扑摘要" in catalog:
        oks.append("A6 catalog 依赖拓扑摘要")
    else:
        fails.append("A6 catalog 缺依赖拓扑摘要")
    files = [p.name for p in refs.glob("BHO-*范本.md")]
    if len(files) == 15:
        oks.append("A1 三层结构：3 索引 + 15 域范本")
    else:
        fails.append(f"A1 域范本数 {len(files)}，应为 15")

    rows = {}
    for line in catalog.splitlines():
        m = ID_RE.match(line)
        if m:
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) >= 6:
                rows[m.group(1)] = c
    total = len(rows)
    if total == 125:
        oks.append("B1 catalog 单元数 125")
    else:
        fails.append(f"B1 单元数 {total}，应为 125")

    bad_dep, entries, idents = [], 0, {}
    for uid, c in rows.items():
        dep = c[3]
        if dep.startswith("无"):
            entries += 1
        for d in ID_ANY.findall(dep):
            if d not in rows:
                bad_dep.append(f"{uid}->{d}")
        if c[5]:
            idents[uid] = c[5]
    if bad_dep:
        fails.append("B4 依赖引用无效: " + "; ".join(bad_dep[:5]))
    else:
        oks.append("B4 依赖引用全部有效")
    ratio = entries / total if total else 1
    if ratio <= 0.30:
        oks.append(f"B5 入口单元 {entries}/{total} = {ratio:.1%}")
    else:
        fails.append(f"B5 入口单元占比 {ratio:.1%} > 30%")

    names = [x.strip() for v in idents.values() for x in v.split("×") if x.strip()]
    dup = sorted({n for n in names if names.count(n) > 1})
    if len(names) == 375 and not dup:
        oks.append("身份 375 条全部唯一（125 主 + 250 协同）")
    else:
        fails.append(f"身份 {len(names)} 条 / 重复 {dup[:5]}")

    miss = []
    for uid in sorted(rows):
        key = f"#### {uid} "
        if key not in reqs:
            miss.append(uid + "(无节)")
            continue
        block = reqs.split(key)[-1].split("\n#### ")[0]
        for s in SLOTS:
            if f"**{s}**" not in block:
                miss.append(f"{uid}:{s}")
    if miss:
        fails.append("C1-C5 槽位缺失: " + ", ".join(miss[:8]))
    else:
        oks.append("C1-C5 125 单元五槽位齐全")

    if "与执行框架的接口" in skill:
        oks.append("D1 SKILL 含与执行框架的接口")
    else:
        fails.append("D1 缺「与执行框架的接口」章节")
    if all(f"Step {i}" in skill for i in range(5)):
        oks.append("D2 覆盖 Step 0–4")
    else:
        fails.append("D2 Step 0–4 不完整")
    if all(f"R{i}" in skill for i in range(1, 6)):
        oks.append("D3 含 R1–R5 领域推导")
    else:
        fails.append("D3 R1–R5 不完整")

    if "## 范本清单" in exem and "| 域 | 范本文件 |" in exem:
        oks.append("E1 exemplars 按域分组清单表")
    else:
        fails.append("E1 exemplars 缺按域清单表")
    if "## 范本模板格式" in exem:
        oks.append("E3 范本模板格式")
    else:
        warns.append("E3 未提供范本模板格式")

    names_cat = {u: c[1] for u, c in rows.items()}
    name_bad, sec_bad, mat_bad, sec_total = [], [], [], 0
    for d in DOMAINS:
        f = list(refs.glob(f"BHO-{d}-*范本.md"))
        if not f:
            fails.append(f"缺 {d} 域范本")
            continue
        text = read(f[0])
        for uid, nm in re.findall(r"(?m)^#### ((?:X0|N[1-4]|B(?:10|[1-9]))-\d{2}) (.+?) ——", text):
            sec_total += 1
            if names_cat.get(uid) != nm:
                name_bad.append(f"{uid}:{nm}")
            block = text.split(f"#### {uid} ")[1].split("\n#### ")[0]
            for s in SECTIONS:
                if f"**{s}**" not in block:
                    sec_bad.append(f"{uid}:{s}")
                    break
            m = re.search(r"\| 槽位 \|(.+?)(?:\n\n|\Z)", block, re.S)
            if not m or sum(1 for s in SLOTS if s in m.group(1)) < 5:
                mat_bad.append(uid)
    if sec_total == total:
        oks.append(f"范本任务节合计 {sec_total} = 单元数")
    else:
        fails.append(f"范本节 {sec_total} ≠ 单元数 {total}")
    if name_bad:
        fails.append("范本任务名与 catalog 不一致: " + ", ".join(name_bad[:5]))
    else:
        oks.append("catalog / requirements / 范本 任务名一致")
    if sec_bad:
        fails.append("范本节 7 要素缺失: " + ", ".join(sec_bad[:6]))
    else:
        oks.append("范本 125 节 7 要素齐全")
    if mat_bad:
        fails.append("覆盖矩阵不足 5 行: " + ", ".join(mat_bad[:6]))
    else:
        oks.append("覆盖矩阵 125 节均含五槽位")

    for sub in ("references", "scripts", "templates"):
        p = root / sub
        if p.exists():
            for ch in p.iterdir():
                if ch.is_dir():
                    fails.append(f"目录超限: {sub}/{ch.name}")
    if not any("目录超限" in f for f in fails):
        oks.append("两级目录合规（内部无子目录）")

    h1 = [p.name for p in refs.glob("*.md") if re.search(r"(?m)^# ", read(p))]
    if h1:
        fails.append("references 内存在一级标题: " + ", ".join(h1[:3]))
    else:
        oks.append("references 无一级标题（层级从 ## 起）")

    dups = []
    for p in root.rglob("*.md"):
        hs = [l for l in read(p).split("\n") if l.startswith("#")]
        for h in set(hs):
            if hs.count(h) > 1 and re.match(r"^#+ \S", h):
                dups.append(f"{p.name}:{h}")
    if dups:
        fails.append("重复标题: " + ", ".join(dups[:3]))
    else:
        oks.append("无重复标题")

    bad_tpl = [p.name for p in (root / "templates").glob("*.md") if read(p).count("${") != read(p).count("}")]
    if bad_tpl:
        fails.append("模板占位符不闭合: " + ", ".join(bad_tpl))
    else:
        oks.append("模板占位符闭合")

    # 样例企业圣经一致性（同企业同批次，跨域数字不得漂移）
    all_fan = "\n".join(read(p) for p in refs.glob("BHO-*范本.md"))
    must = ["420 人", "420,000", "412,000", "9,665.75", "40,000", "134 人", "800 人",
            "2027-01-13", "3,600,000", "1,080,000", "300 元/人月"]
    miss_b = [m for m in must if m not in all_fan]
    ban = ["在岗 300 人", "1,800 人月", "院校 C 300 + 渠道 B 200", "| 客户 B | 120,000",
           "200 人分两波入场", "毛利率 50%", "| 毛利 | 210,000", "3,000 | 0.85",
           "| B | 420 | 70%", "| 院校直供 | 300", "| 毛利 | 1,800,000"]
    hit_b = [b for b in ban if b in all_fan]
    if miss_b or hit_b:
        fails.append(f"圣经不一致：缺 {miss_b[:4]} / 残留 {hit_b[:4]}")
    else:
        oks.append("样例企业圣经一致（同一机构/客户/批次，无漂移值）")

    print("== BHO 自检 ==")
    for x in oks:
        print("[PASS]", x)
    for x in warns:
        print("[WARN]", x)
    for x in fails:
        print("[FAIL]", x)
    print(f"== 结果：{len(oks)} PASS / {len(warns)} WARN / {len(fails)} FAIL ==")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
