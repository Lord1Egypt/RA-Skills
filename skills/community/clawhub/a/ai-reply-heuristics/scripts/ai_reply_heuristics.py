# -*- coding: utf-8 -*-
"""AI痕迹启发式检查器：启发式估计一段文字的 AI 痕迹强度。零依赖。

信号：套话密度 / 破折号频率 / 句长均匀度 / 排比列表占比。
输出 0-100 分与三档区间：<30 更像人写 · 30-60 存疑 · >60 AI 痕迹明显。
免责：启发式提示，不构成"是否 AI 生成"的判定；请勿据此单独追责。
三律映射：LGD-II 有证 —— 出处存疑要有提示。

用法：
  python ai_reply_heuristics.py --file reply.txt
  python ai_reply_heuristics.py --text "..." --json
"""
import argparse, json, pathlib, re, statistics, sys

CLICHE = ["深入探讨", "总而言之", "综上所述", "值得注意的是", "在当今", "随着…的发展",
          "赋能", "抓手", "闭环思维", "delve", "furthermore", "in conclusion",
          "it's important to note", "moreover", "tapestry", "landscape of"]


def score(text):
    n = len(text)
    hits = [c for c in CLICHE if c.lower() in text.lower()]
    s = min(48, 12 * len(hits))
    s += min(24, 8 * len(re.findall(r"——|--", text)))
    sents = [x for x in re.split(r"[。！？!?\n]", text) if len(x.strip()) >= 6]
    if len(sents) >= 4:
        lens = [len(x) for x in sents]
        if statistics.pstdev(lens) < 6:
            s += 15
    lines = [x for x in text.splitlines() if x.strip()]
    if lines and sum(1 for x in lines if re.match(r"\s*[-*\d]+[.、)]", x)) / len(lines) > 0.4:
        s += 13
    s = min(100, s)
    band = "更像人写" if s < 30 else ("存疑" if s <= 60 else "AI 痕迹明显")
    return {"score": s, "band": band, "cliche_hits": hits,
            "sentences": len(sents), "chars": n,
            "note": "启发式提示，不构成判定；单独信号均可能误报"}


def main():
    ap = argparse.ArgumentParser(description="AI痕迹启发式检查器 · AI 痕迹提示器")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="文本文件")
    src.add_argument("--text", help="文本（内联 / @文件 / 纯路径）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        if a.file:
            text = pathlib.Path(a.file).read_text(encoding="utf-8-sig")
        else:
            q = a.text[1:] if a.text.startswith("@") else a.text
            text = pathlib.Path(q).read_text(encoding="utf-8-sig") if pathlib.Path(q).is_file() else q
    except OSError as e:
        print(f"输入不可读：{e}", file=sys.stderr)
        sys.exit(2)
    r = score(text)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"AI 痕迹分：{r['score']}/100（{r['band']}）")
        if r["cliche_hits"]:
            print("命中套话：" + "、".join(r["cliche_hits"][:8]))
        print("免责：" + r["note"])
    sys.exit(0)


if __name__ == "__main__":
    main()
