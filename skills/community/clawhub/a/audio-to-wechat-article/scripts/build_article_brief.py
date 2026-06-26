#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

FILLERS = ["嗯", "然后", "就是", "我觉得", "其实", "那个", "这个", "大家知道吧"]


def clean_text(text: str) -> str:
    for f in FILLERS:
        text = text.replace(f, "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_paras(text: str):
    paras = [p.strip() for p in re.split(r"\n+", text) if p.strip()]
    return paras


def top_sentences(paras, n=8):
    scored = []
    for p in paras:
        score = min(len(p), 300)
        if any(k in p for k in ["所以", "本质", "关键", "核心", "不是", "而是", "意味着"]):
            score += 80
        scored.append((score, p))
    scored.sort(reverse=True)
    return [p for _, p in scored[:n]]


def detect_mode(text: str):
    if any(k in text for k in ["案例", "复盘", "怎么做", "流程", "落地"]):
        return "case-or-practical"
    if any(k in text for k in ["老板", "管理", "创业", "商业化"]):
        return "boss-facing"
    return "insight"


def main():
    if len(sys.argv) < 2:
        print("Usage: build_article_brief.py <input.txt|md> [output.json]")
        sys.exit(1)
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else inp.with_suffix('.brief.json')
    raw = inp.read_text(encoding='utf-8', errors='ignore')
    text = clean_text(raw)
    paras = split_paras(text)
    data = {
        "source_path": str(inp),
        "mode_guess": detect_mode(text),
        "paragraph_count": len(paras),
        "top_points": top_sentences(paras, 8),
        "first_paragraph": paras[0] if paras else "",
        "last_paragraph": paras[-1] if paras else "",
    }
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(str(out))

if __name__ == '__main__':
    main()
