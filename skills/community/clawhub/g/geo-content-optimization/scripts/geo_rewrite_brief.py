#!/usr/bin/env python3
import json, re, sys
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore').strip()


def first_nonempty_paragraphs(text, n=3):
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    return paras[:n]


def pick_title(text):
    m = re.search(r'^(#\s+.+)$', text, re.M)
    if m:
        return m.group(1).lstrip('#').strip()
    return first_nonempty_paragraphs(text, 1)[0][:32] if text else '未命名内容'


def main():
    if len(sys.argv) < 2:
        print('Usage: geo_rewrite_brief.py <file>')
        sys.exit(1)
    p = Path(sys.argv[1])
    text = read_text(p)
    title = pick_title(text)
    paras = first_nonempty_paragraphs(text, 3)
    core = paras[0] if paras else ''
    result = {
        'file': str(p),
        'title_guess': title,
        'top_issue_guess': '开头可能不够直接，需补定义/判断/适合谁',
        'rewrite_targets': [
            '前 3 句说清是什么、适合谁、为什么重要',
            '补 3-5 个 query-shaped 小标题',
            '补 FAQ / 对比 / 结论块',
            '提高可摘录句密度',
            '降低空泛表达比例'
        ],
        'suggested_sections': [
            'What is X / 这是什么',
            'Why it matters / 为什么重要',
            'Who it is for / 适合谁',
            'X vs Y / 和谁比',
            'FAQ / 常见问题',
            'Verdict / 一句话结论'
        ],
        'opening_paragraphs': paras,
        'quoteable_line_example': f'真正值钱的，不是“{title}”这个说法，而是它背后更容易被 AI 提取、引用和推荐的表达结构。'
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
