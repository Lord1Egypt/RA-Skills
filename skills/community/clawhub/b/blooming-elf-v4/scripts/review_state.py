#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
review_state.py — 绿灵·Blooming Elf-v4 复查脚本（v4.0.4 新增）

用途：
  1. 读 plants.json 跑一致性校验（日期/key/last≤next/status/category/数量/间隔/microclimate 缺失过期）。
  2. 支持 --ima <md> 最佳努力解析「小森林风格」markdown 档案，交叉核对盆数、🔴已弃、格式。

退出码：
  0 = 无错误（⚠️ 警告仍会打印，但不影响退出码）
  1 = 存在 ❌ 错误（数据不健康）

仅用标准库，无外部依赖。
"""

import argparse
import json
import re
import sys
from datetime import date, datetime

VALID_STATUS = {"正常", "休眠", "停水观察", "已弃"}
VALID_CATEGORIES = {"土培", "吸水盆", "水培", "鲜切花", "水养"}
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _today():
    return date.today()


def _parse_iso(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def _errs(report, level, msg):
    report[level].append(msg)


def review_plants_json(path):
    """返回 (report_dict, exit_code)"""
    report = {"❌": [], "⚠️": [], "✅": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        _errs(report, "❌", f"无法读取/解析 JSON：{e}")
        return report, 1

    # 归一实例
    instances = data.get("instances")
    if not instances:
        # 兼容单实例 legacy
        if "plants" in data:
            instances = [{
                "elf": data.get("user", "未知"),
                "location": data.get("location", ""),
                "microclimate": data.get("microclimate"),
                "plants": data["plants"],
            }]
        else:
            _errs(report, "❌", "未找到 instances[] 或顶层 plants[]")
            return report, 1

    seen_keys = set()
    alive = 0
    discarded = 0
    total = 0

    for inst in instances:
        elf = inst.get("elf", "未知")
        loc = inst.get("location", "")
        plants = inst.get("plants", [])
        seen_keys = set()  # key 唯一性按实例内判定（家里/公司可同名）
        # microclimate 检查
        mc = inst.get("microclimate")
        if not mc or mc.get("source") != "实测":
            _errs(report, "⚠️", f"[{elf}/{loc}] 缺实测环境档案(microclimate)，浇水/喷雾将降级用城市天气")
        else:
            ma = _parse_iso(mc.get("measured_at", ""))
            if ma is None:
                _errs(report, "⚠️", f"[{elf}/{loc}] microclimate.measured_at 格式错：{mc.get('measured_at')}")
            elif (date.today() - ma).days > 7:
                _errs(report, "⚠️", f"[{elf}/{loc}] microclimate 实测过期(>{ (date.today()-ma).days }天)，降级城市天气")

        for p in plants:
            total += 1
            key = p.get("key", "")
            name = p.get("name", key)
            status = p.get("status", "正常")
            cat = p.get("category", "")

            if not key:
                _errs(report, "❌", f"[{elf}] 植物缺 key：{name}")
            elif key in seen_keys:
                _errs(report, "❌", f"[{elf}] key 重复：{key}")
            else:
                seen_keys.add(key)

            if status not in VALID_STATUS:
                _errs(report, "❌", f"[{elf}] {key} status 非法：{status}")
            if cat not in VALID_CATEGORIES:
                _errs(report, "❌", f"[{elf}] {key} category 非法：{cat}")
            if status == "已弃":
                discarded += 1
            else:
                alive += 1

            lw = p.get("last_water")
            nw = p.get("next_water")
            for dfield in ("last_water", "next_water", "fertilizer_last", "fertilizer_next", "bought_at"):
                v = p.get(dfield)
                if v and not ISO_RE.match(str(v)):
                    _errs(report, "❌", f"[{elf}] {key} {dfield} 非 ISO 日期：{v}")
            if lw and nw:
                d1, d2 = _parse_iso(lw), _parse_iso(nw)
                if d1 and d2:
                    if d2 < d1:
                        _errs(report, "❌", f"[{elf}] {key} next_water({nw}) < last_water({lw})")
                    else:
                        diff = (d2 - d1).days
                        cap = p.get("water_interval_max")
                        if cap and isinstance(cap, int) and diff > cap * 1.5:
                            _errs(report, "⚠️", f"[{elf}] {key} 间隔 {diff} 天 > 上限参考 {cap}×1.5；与'控水偏干'类备注矛盾时检查")
                        if diff == 0:
                            _errs(report, "⚠️", f"[{elf}] {key} 上次=下次({lw})，疑似未更新")

    _errs(report, "✅", f"总计 {total} 盆：存活 {alive}（不含已弃）、已弃 {discarded}")
    exit_code = 1 if report["❌"] else 0
    return report, exit_code


def review_ima_md(path):
    """最佳努力解析小森林风格 markdown，交叉核对。返回 report_dict（仅 ⚠️/✅，不致命）。"""
    report = {"❌": [], "⚠️": [], "✅": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        _errs(report, "⚠️", f"IMA 文档读取失败：{e}")
        return report

    section = None
    counts = {}
    cut_red = 0
    cut_red_with_days = 0
    md_date_rows = 0  # 含 M/D 非 ISO 的疑似日期行

    for ln in lines:
        s = ln.strip()
        if s.startswith("##"):
            if "土培" in s:
                section = "土培"
            elif "吸水盆" in s:
                section = "吸水盆"
            elif "水培" in s or "水养" in s:
                section = "水培"
            elif "鲜切" in s:
                section = "鲜切花"
            else:
                section = None
            continue
        if not s.startswith("|"):
            continue
        if re.match(r"^\|[\-\|]+\|$", s):  # 分隔行
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells or not cells[0]:
            continue
        if section in ("土培", "吸水盆", "水培", "鲜切花"):
            counts[section] = counts.get(section, 0) + 1
        # 检测 M/D 格式日期（非 ISO）
        for c in cells:
            if re.match(r"^\d{1,2}/\d{1,2}$", c):
                md_date_rows += 1
                break
        if section == "鲜切花":
            row = " ".join(cells)
            if "🔴" in row:
                cut_red += 1
                # 找第一个纯数字作为存活天数
                m = re.search(r"\|(\d+)\|", s)
                if m:
                    cut_red_with_days += 1

    _errs(report, "✅", f"IMA 文档分段盆数：土培 {counts.get('土培',0)} / 吸水盆 {counts.get('吸水盆',0)} / 水培 {counts.get('水培',0)} / 鲜切花 {counts.get('鲜切花',0)}")
    if md_date_rows:
        _errs(report, "⚠️", f"检测到 {md_date_rows} 处 M/D 格式日期（非 ISO）；同步到 plants.json 时由 migrate 工具转 ISO")
    if cut_red:
        _errs(report, "✅", f"鲜切花 🔴 已弃 {cut_red} 支（其中 {cut_red_with_days} 支保留存活天数——用于判断品种耐久，属故意保留，非错误）")
    return report


def _print(report):
    for lvl in ("❌", "⚠️", "✅"):
        for m in report[lvl]:
            print(f"{lvl} {m}")
    if not report["❌"] and not report["⚠️"]:
        print("✅ 全部通过，无告警")


def main():
    ap = argparse.ArgumentParser(description="绿灵 v4 复查脚本")
    ap.add_argument("state", nargs="?", help="plants.json 路径")
    ap.add_argument("--ima", help="小森林风格 markdown 档案路径（最佳努力交叉核对）")
    args = ap.parse_args()

    if not args.state and not args.ima:
        ap.print_help()
        sys.exit(2)

    code = 0
    if args.state:
        rep, c = review_plants_json(args.state)
        print("=== plants.json 校验 ===")
        _print(rep)
        code = max(code, c)
    if args.ima:
        rep = review_ima_md(args.ima)
        print("\n=== IMA 文档交叉核对 ===")
        _print(rep)
    sys.exit(code)


if __name__ == "__main__":
    main()
