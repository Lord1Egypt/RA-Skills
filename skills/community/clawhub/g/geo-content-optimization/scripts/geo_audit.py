#!/usr/bin/env python3
import re, sys, json
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore')


def count(pattern, text, flags=re.I):
    return len(re.findall(pattern, text, flags))


def main():
    if len(sys.argv) < 2:
        print('Usage: geo_audit.py <file>')
        sys.exit(1)
    p = Path(sys.argv[1])
    text = read_text(p)
    low = text.lower()

    headings = count(r'^(#|##|###|<h1|<h2|<h3)', text, flags=re.I | re.M)
    faq = 'faq' in low or '常见问题' in text
    comparison = ' vs ' in low or '对比' in text or 'alternatives' in low or '替代' in text
    definition = bool(re.search(r'\b(is|are)\b', low[:1200])) or '是什么' in text[:1200]
    bullets = count(r'^\s*[-*•]\s+', text, flags=re.M)
    table = '|' in text or '<table' in low
    dates = count(r'20\d{2}', text)
    questions = count(r'\?', text) + count(r'？', text)

    weaknesses = []
    if headings < 3:
        weaknesses.append('Too few query-aligned headings')
    if not faq:
        weaknesses.append('Missing FAQ / common questions block')
    if not comparison:
        weaknesses.append('Missing comparison / alternatives framing')
    if not definition:
        weaknesses.append('Weak or unclear definition near the top')
    if bullets < 4:
        weaknesses.append('Low extractability: too few bullets/lists')
    if not table:
        weaknesses.append('No table detected; comparison content may be weak')
    if dates == 0:
        weaknesses.append('No date context; freshness may be unclear')

    score = 100
    score -= min(len(weaknesses) * 12, 72)
    if questions > 4:
        score += 4
    if bullets > 10:
        score += 4
    score = max(0, min(100, score))

    result = {
        'file': str(p),
        'geo_score': score,
        'signals': {
            'headings': headings,
            'faq': faq,
            'comparison': comparison,
            'definition_near_top': definition,
            'bullets': bullets,
            'table': table,
            'dates_found': dates,
            'questions_found': questions,
        },
        'top_weaknesses': weaknesses[:5],
        'rewrite_priorities': [
            'Add a direct answer / definition block near the top',
            'Add query-shaped H2 headings',
            'Add comparison and FAQ sections',
            'Increase bullet/table extractability',
            'Add freshness/date context where relevant'
        ]
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
