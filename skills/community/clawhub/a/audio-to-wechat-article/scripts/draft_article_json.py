#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

HOOK_PATTERNS = ['不是', '而是', '关键', '本质', '真正', '意味着']


def pick_core(text: str) -> str:
    paras = [p.strip() for p in re.split(r'\n+', text) if p.strip()]
    if not paras:
        return '未提取到核心观点'
    scored = []
    for p in paras:
        score = min(len(p), 220)
        if any(k in p for k in HOOK_PATTERNS):
            score += 120
        scored.append((score, p))
    scored.sort(reverse=True)
    return scored[0][1]


def make_title(core: str) -> str:
    core = re.sub(r'[。！？!?.].*$', '', core).strip()
    return core[:28] if core else '未命名文章'


def main():
    if len(sys.argv) < 3:
        print('Usage: draft_article_json.py <source.txt> <output.json>')
        sys.exit(1)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    text = src.read_text(encoding='utf-8', errors='ignore').strip()
    core = pick_core(text)
    title = make_title(core)
    summary = core[:90]
    body = f"# {title}\n\n{core}\n\n先说结论：这段内容值得被写成公众号文章，不是因为信息多，而是因为它有一个可以被提炼的核心判断。\n\n## 为什么这件事值得写\n\n把原始录音或文字稿直接发出去，通常是不可读的。真正值钱的是先提炼核心观点，再把它改造成适合公众号阅读的结构。\n\n## 这篇后续应该怎么扩\n\n- 补一个更强的开头钩子\n- 拆成 3-5 个主体部分\n- 加上案例或截图\n- 最后给出一句收束判断\n"
    data = {'title': title, 'summary': summary, 'body': body, 'core_point': core}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(str(out))

if __name__ == '__main__':
    main()
