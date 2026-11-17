#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""copy_compliance.py —— 广告法违禁词 / 极限词 / 平台风险词检测

词库：assets/forbidden_words.json（P0 极限违禁 / P1 需资质 / P2 建议优化 / exempt 豁免短语）

用法：
  python copy_compliance.py --self-test
  python copy_compliance.py --file 详情页.txt --platform tb
  python copy_compliance.py --text "全网最好的XX，第一步这样做" --json
  python copy_compliance.py --file a.txt --allow "全网最低" --json   # 临时加白（需人工签字确认）
退出码：0 无 P0；1 命中 P0（致命）；2 输入缺失。
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORDLIB = os.path.join(os.path.dirname(HERE), "assets", "forbidden_words.json")

LEVEL_TXT = {"P0": "违禁/极限词（必须改）", "P1": "高风险（需资质或证据）", "P2": "建议优化"}


def load_lib(path=None):
    p = path or WORDLIB
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _protected_ranges(text, exempt):
    """返回豁免短语覆盖的字符区间列表"""
    ranges = []
    for e in exempt:
        for phrase in e.get("allow", []):
            start = 0
            while True:
                i = text.find(phrase, start)
                if i < 0:
                    break
                ranges.append((i, i + len(phrase)))
                start = i + 1
    return ranges


def scan(text, lib=None, extra_allow=None):
    lib = lib or load_lib()
    exempt = list(lib.get("exempt") or [])
    if extra_allow:
        exempt.append({"word": "__allow", "allow": list(extra_allow)})
    prot = _protected_ranges(text, exempt)

    hits = []
    for lvl in ("P0", "P1", "P2"):
        for item in lib.get(lvl, []):
            w = item["word"]
            if not w:
                continue
            start = 0
            while True:
                i = text.find(w, start)
                if i < 0:
                    break
                start = i + 1
                if any(a <= i < b for (a, b) in prot):
                    continue
                line = text.count("\n", 0, i) + 1
                col = i - (text.rfind("\n", 0, i) + 1) + 1
                ctx = text[max(0, i - 12): i + len(w) + 12].replace("\n", " ")
                hits.append({"level": lvl, "word": w, "pos": i, "line": line, "col": col,
                             "context": ctx, "alt": item.get("alt", ""), "reason": item.get("reason", "")})
    order = {"P0": 0, "P1": 1, "P2": 2}
    hits.sort(key=lambda h: (order[h["level"]], h["pos"]))
    counts = {lvl: sum(1 for h in hits if h["level"] == lvl) for lvl in ("P0", "P1", "P2")}
    return {"counts": counts, "total": len(hits), "hits": hits,
            "verdict": "FAIL-P0" if counts["P0"] else ("WARN" if counts["P1"] or counts["P2"] else "PASS")}


def render(res, platform=None):
    o = ["【文案合规检测】%s命中 %d 处：P0 %d / P1 %d / P2 %d → %s" % (
        ("平台=" + platform + " " if platform else ""), res["total"],
        res["counts"]["P0"], res["counts"]["P1"], res["counts"]["P2"], res["verdict"])]
    cur = None
    for h in res["hits"]:
        if h["level"] != cur:
            cur = h["level"]
            o.append("  ── %s ──" % LEVEL_TXT[cur])
        o.append("    第%d行第%d列  「%s」  →  建议改为「%s」  （%s）" % (
            h["line"], h["col"], h["word"], h["alt"] or "（删除）", h["reason"]))
        o.append("      上下文：…%s…" % h["context"])
    if not res["hits"]:
        o.append("  未命中词库。注意：通过词库≠绝对合规，功效/医疗/保健类仍需资质。")
    return "\n".join(o)


def self_test() -> int:
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    text = "全网最佳品质，第一品牌保证。第一步：打开包装。医生推荐，加微信领券。第二步完成。"
    res = scan(text)
    p0 = [h["word"] for h in res["hits"] if h["level"] == "P0"]
    p1 = [h["word"] for h in res["hits"] if h["level"] == "P1"]
    p2 = [h["word"] for h in res["hits"] if h["level"] == "P2"]
    chk("命中 P0=最佳", "最佳" in p0)
    chk("命中 P0=第一品牌", "第一品牌" in p0)
    chk("豁免短语「第一步」未误报", not any(w == "第一" for w in p0))
    chk("命中 P1=医生推荐", "医生推荐" in p1)
    chk("命中 P2=加微信", "加微信" in p2)
    chk("verdict=FAIL-P0", res["verdict"] == "FAIL-P0")
    chk("位置定位正确", any(h["word"] == "最佳" and h["line"] == 1 for h in res["hits"]))

    clean = scan("本店新款上架，支持7天无理由退换，材质为纯棉。")
    chk("干净文案 PASS", clean["verdict"] == "PASS")
    chk("--allow 白名单生效", scan("全网最低价", extra_allow=["全网最低价"])["counts"]["P0"] == 0)
    print("copy_compliance self-test: %s" % ("ALL PASS" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="广告法违禁词/极限词检测")
    ap.add_argument("--text", help="待检文本")
    ap.add_argument("--file", help="待检文本文件")
    ap.add_argument("--platform", help="平台：tb/tmall/jd/pdd/douyin/xhs/ks/wx")
    ap.add_argument("--lib", help="自定义词库 JSON")
    ap.add_argument("--allow", action="append", help="临时加白短语，可多次")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if a.file:
        with open(a.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif a.text:
        text = a.text
    else:
        ap.error("需要 --text 或 --file 或 --self-test")
        return 2

    res = scan(text, load_lib(a.lib) if a.lib else None, a.allow)
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else render(res, a.platform))
    return 1 if res["counts"]["P0"] else 0


if __name__ == "__main__":
    sys.exit(main())
