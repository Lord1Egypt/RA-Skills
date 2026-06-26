#!/usr/bin/env python3
import json, re, sys
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore').strip()


def paragraphs(text: str):
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def title_guess(text: str):
    m = re.search(r'^(#\s+.+)$', text, re.M)
    if m:
        return m.group(1).lstrip('#').strip()
    ps = paragraphs(text)
    return ps[0][:28] if ps else '未命名内容'


def first_claim(text: str):
    ps = paragraphs(text)
    return ps[0] if ps else '请补一句最直接的定义或判断。'


def main():
    if len(sys.argv) < 2:
        print('Usage: geo_rewrite_output.py <file>')
        sys.exit(1)
    p = Path(sys.argv[1])
    text = read_text(p)
    title = title_guess(text)
    claim = first_claim(text)
    output = {
        'file': str(p),
        'new_title_candidates': [
            f'{title}：真正值钱的，不是流量，而是进入答案本身',
            f'为什么说“{title}”这件事，应该按 GEO 重写',
            f'{title}：怎么改，才更容易被 ChatGPT / Claude / Gemini 引用'
        ],
        'better_opening': [
            '先用 1 句话说清它是什么。',
            '再用 1 句话说清它适合谁。',
            '再用 1 句话说清为什么值得看。'
        ],
        'definition_block': f'{title} 不是一个空概念，它更适合被理解为：让内容更容易被大模型提取、引用、推荐的一套内容结构优化方法。',
        'comparison_block': [
            {'维度': '传统 SEO', '重点': '搜索结果排名'},
            {'维度': 'GEO', '重点': '进入 AI 生成的答案本身'}
        ],
        'faq_block': [
            'GEO 是什么？',
            'GEO 和 SEO 有什么区别？',
            '什么内容最适合做 GEO？',
            '为什么很多文章不容易被 AI 引用？',
            '第一步应该怎么改？'
        ],
        'verdict_block': '真正值钱的，不是你写了多少内容，而是你的内容能不能进入答案本身。',
        'source_hint': claim[:200]
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
