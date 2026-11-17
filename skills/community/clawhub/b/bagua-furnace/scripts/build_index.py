#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描方法论卡库，生成单一索引 INDEX.md（按 pattern 聚类）。

支持两类卡，一视同仁解析 v2 路由头：
  - deep_*.md   ：深卡（路由层 + 理解层）
  - harbor_*.md ：方法卡（每张可含 1–3 个方法块，每块自带一个 frontmatter 路由头）

一张卡含多个方法块时，**全部**入索引（旧版只取第一个，会丢掉 2/3 的方法）。
无 frontmatter 的卡降级列入"待补路由头"，不参与聚类。

用法：
  python build_index.py
"""
import os, re, glob

LIB = os.path.expanduser(r"C:\Users\zyd\.workbuddy\methodology-library")
OUT = os.path.join(LIB, "INDEX.md")

REQUIRED_PATTERNS = []  # 不强制，仅统计


def as_text(v):
    """frontmatter 的值可能是列表（deep 卡用 `key: ['a','b']` 或 '- ' 列表块），统一转文本。"""
    if isinstance(v, list):
        return "；".join(str(x) for x in v)
    return str(v) if v is not None else ""


def _parse_block(block):
    """解析单个 frontmatter 块的键值，支持 ['a','b'] 与 '- ' 列表块。"""
    meta = {}
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            if val.startswith("["):
                inner = val.strip("[]").strip()
                meta[key] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()] if inner else []
            elif val == "":
                # 列表块：后续以 '- ' 开头的行
                items = []
                j = i + 1
                while j < len(lines) and lines[j].lstrip().startswith("- "):
                    items.append(lines[j].lstrip()[2:].strip())
                    j += 1
                meta[key] = items
                i = j
                continue
            else:
                meta[key] = val
        i += 1
    return meta


def parse_all_frontmatter(text):
    """解析【全部】frontmatter 块（一张卡可含多个方法块），并各自关联方法名。

    ⚠️ 切勿改回 `re.match(r"^---...")` 只取第一个。旧实现有两个 bug：
       ① `^` 锚定文件头——卡顶部有 H1 标题时解析直接失败；
       ② 只取首个块——每张卡后 2 个方法块（占全部方法的 2/3）永远进不了索引。
    """
    entries = []
    parts = re.split(r"---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    for i in range(1, len(parts), 2):
        meta = _parse_block(parts[i])
        body = parts[i + 1] if i + 1 < len(parts) else ""
        mm = re.search(r"#\s*【名称】\s*(.+)", body)
        meta["_method"] = mm.group(1).strip() if mm else ""
        # 方法块标题在部分卡里写作 `# 【名称】`，也有 `## 【名称】`，上面已兼容
        if meta:
            entries.append(meta)
    return entries


def parse_frontmatter(text):
    """兼容旧调用：返回第一个 frontmatter 块（无则空）。新代码请用 parse_all_frontmatter。"""
    all_fm = parse_all_frontmatter(text)
    return all_fm[0] if all_fm else {}


def title_of(path, text):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        return m.group(1).strip()
    return os.path.basename(path)


def main():
    # 两类卡一视同仁：不再把 harbor_*.md 当成"薄卡"只列文件名
    cards = sorted(glob.glob(os.path.join(LIB, "deep_*.md"))) + \
            sorted(glob.glob(os.path.join(LIB, "harbor_*.md")))

    entries = []   # 每个方法块一条
    plain = []     # 无任何 frontmatter 的卡（降级列名）

    for p in cards:
        text = open(p, encoding="utf-8").read()
        fms = parse_all_frontmatter(text)
        if not fms:
            plain.append(os.path.basename(p))
            continue
        for fm in fms:
            entries.append({
                "file": os.path.basename(p),
                "title": title_of(p, text),
                "method": fm.get("_method", ""),
                "pattern": as_text(fm.get("pattern")) or "未分类",
                "pattern_raw": as_text(fm.get("pattern_raw", "")),
                "trigger": as_text(fm.get("trigger", "")),
                "root_cause": as_text(fm.get("root_cause", "")),
                "surface_domain": as_text(fm.get("surface_domain", "")),
                "confidence": as_text(fm.get("confidence", "-" )),
                "source_fidelity": as_text(fm.get("source_fidelity", "-")),
            })

    by_pattern = {}
    for e in entries:
        by_pattern.setdefault(e["pattern"], []).append(e)

    n_deep = len(glob.glob(os.path.join(LIB, "deep_*.md")))
    n_harbor = len(glob.glob(os.path.join(LIB, "harbor_*.md")))

    L = []
    L.append("# 方法论卡库索引 INDEX\n")
    L.append(f"> 自动生成（八卦炉 `scripts/build_index.py`）。共 **{len(cards)}** 张卡"
             f"（深卡 {n_deep} + 方法卡 {n_harbor}）/ **{len(entries)}** 个方法块，"
             f"归并为 **{len(by_pattern)}** 个 pattern 聚类。\n")
    L.append("> 取招路径：按「症状或根因」定位 pattern 聚类 → 聚类内按 trigger 挑最贴的方法 → 打开对应卡读全文。\n")
    L.append("> `原名` 为该方法的原始模式词（卡内 `pattern_raw` 字段），便于追溯归并前语义。\n")
    L.append("\n## 一、按 pattern 聚类（扫地僧「博览」入口）\n")

    for pat in sorted(by_pattern):
        items = by_pattern[pat]
        L.append(f"\n### pattern: {pat}  （{len(items)} 个方法）\n")
        for e in items:
            L.append(
                "- 卡：`{file}` ｜ 方法：{method} ｜ 原名：{raw} ｜ trigger：{trg} ｜ "
                "root_cause：{rc} ｜ surface_domain：{sd} ｜ confidence：{cf} ｜ source_fidelity：{sf}".format(
                    file=e["file"],
                    method=e["method"] or "—",
                    raw=e["pattern_raw"] or "—",
                    trg=e["trigger"] or "（未填触发）",
                    rc=e["root_cause"] or "—",
                    sd=e["surface_domain"] or "—",
                    cf=e["confidence"],
                    sf=e["source_fidelity"],
                )
            )

    if plain:
        L.append("\n## 二、无路由头的卡（未入聚类，待补 v2 路由头）\n")
        for f in plain:
            L.append(f"- {f}\n")

    L.append("\n## 三、统计\n")
    L.append(f"- 卡：{len(cards)} 张（深卡 {n_deep} ＋ 方法卡 {n_harbor}）\n")
    L.append(f"- 方法块：{len(entries)} 个 ｜ pattern 聚类：{len(by_pattern)} 个 ｜ 无路由头：{len(plain)} 张\n")

    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print(f"INDEX 已生成：{OUT}")
    print(f"卡 {len(cards)} 张 ｜ 方法块 {len(entries)} 个 ｜ pattern 聚类 {len(by_pattern)} 个 ｜ 无路由头 {len(plain)} 张")


if __name__ == "__main__":
    main()
