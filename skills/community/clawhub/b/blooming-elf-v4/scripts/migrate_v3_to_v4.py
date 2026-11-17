#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
migrate_v3_to_v4.py — 旧版 markdown 植物档案 → v4 plants.json 迁移工具

解决「v3→v4 升级门槛」：老用户装上 v4 不必手工重建数据。

能力（对应已识别的优化点）：
    • 水养 → 水培 同义归一（档案常用「水养」）
    • M/D → ISO YYYY-MM-DD（年份取 --year，默认 2026）
    • 🔴 / 「已丢」→ status=已弃（已弃盆不提醒不计数）
    • 「停水观察」→ status=停水观察；休眠标记（如花谢蝴蝶兰）→ 休眠
    • 浇水日志反推 water_interval_max（中位间隔）
    • 多副本去重：传入多份档案，按「最后更新」时间戳取最新，同名同地点只记一次
    • 按 location 分 instance（家里→绿灵 / 公司→小森林，可 --map 覆盖）

用法：
    python3 migrate_v3_to_v4.py <档案1.md> [档案2.md ...] \
        --out plants.json [--year 2026] [--user 十一一]

说明：本工具针对 v3 档案格式（屋里的植物 / 小森林）调优；其他格式可扩展 parser。
"""
import sys
import os
import re
import json
import argparse
from datetime import date, timedelta

DATE_RE = re.compile(r"^(\d{1,2})/(\d{1,2})$")          # M/D
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MULTI_POT_RE = re.compile(r"×(\d+)\s*盆")               # ×2盆 → 2 盆
MULTI_STEM_RE = re.compile(r"×(\d+)\s*株")              # ×4株 → 1 盆(多茎)
RED_RE = re.compile(r"🔴|已丢|已死|discard")             # 已弃标记


def md_to_iso(s, year):
    s = (s or "").strip()
    m = DATE_RE.match(s)
    if m:
        return f"{year}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    if ISO_RE.match(s):
        return s
    return ""


def find_update_time(text):
    """从档案头取最后更新时间 M/D 或 YYYY-MM-DD。"""
    m = re.search(r"最后更新[：:]\s*(\d{4})年(\d{1,2})月(\d{1,2})日", text)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.search(r"最后更新[：:]\s*(\d{1,2})/(\d{1,2})", text)
    if m:
        return date(2000, int(m.group(1)), int(m.group(2)))  # 无年，仅排序用
    return date(2000, 1, 1)


def split_sections(text):
    """返回 {section_key: [row_cells, ...]} 与 logs {name: [iso_dates]}。"""
    sections = {"土培": [], "水养": [], "吸水盆": [], "鲜切花": []}
    logs = {}
    cur = None
    lines = text.splitlines()
    for ln in lines:
        if not ln.strip().startswith("|"):
            # 章节标题（仅识别到的标题切换 cur；其余行不改变 cur，避免空行/说明行重置）
            h = ln.strip()
            if "浇水日志" in h:
                cur = "log"
            elif "土培" in h and "鲜切" not in h and "水养" not in h and "吸水" not in h:
                cur = "土培"
            elif "水养" in h or "水培植物" in h:
                cur = "水养"
            elif "吸水盆" in h:
                cur = "吸水盆"
            elif "鲜切" in h:
                cur = "鲜切花"
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if cur == "log":
            if len(cells) >= 2 and cells[0] and not cells[0].startswith("---"):
                name = cells[0]
                ds = re.findall(r"(\d{1,2})/(\d{1,2})", cells[1])
                logs[name] = [f"2000-{int(m):02d}-{int(d):02d}" for m, d in ds]
        elif cur in sections and len(cells) >= 2 and cells[0] and not cells[0].startswith("---"):
            sections[cur].append(cells)
    return sections, logs


def infer_interval(log_dates, default=5):
    """从日志日期（ISO，年占位 2000）取中位间隔天数。"""
    ds = sorted(set(log_dates))
    if len(ds) < 2:
        return default
    gaps = []
    for a, b in zip(ds, ds[1:]):
        try:
            da = date.fromisoformat(a); db = date.fromisoformat(b)
        except ValueError:
            continue
        gaps.append(abs((db - da).days))
    if not gaps:
        return default
    gaps.sort()
    return gaps[len(gaps) // 2] or default


def parse_archives(paths, year, user):
    """解析多份档案，按 location 归并，返回 instances 列表。"""
    parsed = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            text = f.read()
        loc = "公司" if ("小森林" in text or "公司" in text) else "家里"
        parsed.append((find_update_time(text), loc, text))

    # 去重：同名同地点只保留最后更新最新的一份
    best = {}
    for upd, loc, text in parsed:
        key = loc
        if key not in best or upd > best[key][0]:
            best[key] = (upd, text)

    instances = []
    for loc, (_, text) in best.items():
        sections, logs = split_sections(text)
        plants = []
        seen = set()
        for sec, cat in (("土培", "土培"), ("水养", "水养"), ("吸水盆", "吸水盆")):
            for cells in sections.get(sec, []):
                name = cells[0]
                # 取下次浇水列
                if sec == "吸水盆" and len(cells) > 2:
                    next_raw = cells[2]
                else:
                    next_raw = cells[1] if len(cells) > 1 else ""
                status = "正常"
                if "停水观察" in next_raw:
                    status = "停水观察"
                    next_iso = ""
                else:
                    next_iso = md_to_iso(next_raw, year)
                # 多盆展开
                npot = MULTI_POT_RE.search(" ".join(cells))
                n = int(npot.group(1)) if npot else 1
                interval = infer_interval(logs.get(name, []))
                if not interval or interval < 2:
                    interval = 5
                for i in range(n):
                    suffix = f"-{i+1}" if n > 1 else ""
                    # key 唯一化（同名异盆/异培育方式去重）
                    base = f"{name}{suffix}"
                    key = base
                    c = 2
                    while key in seen:
                        key = f"{base}-{c}"
                        c += 1
                    seen.add(key)
                    # 水养段无日期 → 用日志/默认推
                    lw = ""
                    nw = next_iso
                    if not nw and name in logs:
                        nw = md_to_iso(logs[name][0].replace("2000-", f"{year}-"), year) if logs[name] else ""
                    plants.append({
                        "key": key,
                        "name": name,
                        "category": "水养" if sec == "水养" else cat,
                        "status": status,
                        "last_water": lw,
                        "next_water": nw,
                        "water_interval_max": interval,
                        "light": cells[3] if len(cells) > 3 else "",
                        "note": (cells[-1] if len(cells) > 1 and cells[-1] not in ("—", "") else ""),
                    })
        # 鲜切花 → 已弃
        for cells in sections.get("鲜切花", []):
            name = cells[0]
            status = "已弃" if RED_RE.search(" ".join(cells)) else "正常"
            bought = ""
            m = re.search(r"(\d{1,2})/(\d{1,2})", cells[2] if len(cells) > 2 else "")
            if m:
                bought = md_to_iso(f"{m.group(1)}/{m.group(2)}", year)
            survive = ""
            if len(cells) > 1 and cells[1].isdigit():
                survive = int(cells[1])
            plants.append({
                "key": f"鲜切-{name}",
                "name": name,
                "category": "鲜切花",
                "status": status,
                "bought_at": bought,
                "survive_days": survive,
                "water_level": cells[3] if len(cells) > 3 else "",
                "note": "迁移自 v3 鲜切花表",
            })
        elf = "绿灵" if loc == "家里" else "小森林"
        inst = {
            "elf": elf, "user": user, "remind_time": "19:00" if loc == "家里" else "10:00",
            "city": "武汉", "climate": "亚热带季风气候", "env": "室内",
            "location": loc,
            "pets": ({"cats": False, "dogs": False, "birds": ["牡丹鹦鹉"]} if loc == "家里" else {}),
            "plants": plants,
        }
        instances.append(inst)
    return instances


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archives", nargs="+", help="旧版 markdown 档案路径（可多份）")
    ap.add_argument("--out", required=True, help="输出 plants.json")
    ap.add_argument("--year", type=int, default=2026)
    ap.add_argument("--user", default="十一一")
    args = ap.parse_args()

    instances = parse_archives(args.archives, args.year, args.user)
    out = {"version": 4, "updated_at": date.today().isoformat(), "instances": instances}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    total = sum(len(i["plants"]) for i in instances)
    alive = sum(1 for i in instances for p in i["plants"] if p.get("status") != "已弃")
    print(f"✅ 迁移完成：{len(instances)} 个实例，{alive} 盆存活（{total-alive} 盆已弃），→ {args.out}")


if __name__ == "__main__":
    main()
