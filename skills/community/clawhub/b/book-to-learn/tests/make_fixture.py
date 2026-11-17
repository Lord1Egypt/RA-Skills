#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_fixture.py — 生成一个「离线可跑」的测试用数据目录

用途：不碰真实数据、不需要任何推送凭据，就能验证推送流程
（首次启动门禁 / 批量取载荷 / 标记进度 / 校验）。

用法：
    python tests/make_fixture.py --slug _fixture [--cards 3]

生成 books/<slug>/：config.json（confirmed 全 false，用于演示门禁）、
items.json、index.json、progress.json。跑完可直接删掉该目录。
"""
import argparse
import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_DIR)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--slug', default='_fixture')
    ap.add_argument('--cards', type=int, default=3)
    a = ap.parse_args()

    bd = os.path.join(SKILL_DIR, 'books', a.slug)
    os.makedirs(bd, exist_ok=True)

    cfg_path = os.path.join(SKILL_DIR, 'config.example.json')
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    cfg.update({'bookTitle': '示例来源（测试用）', 'bookSlug': a.slug, 'language': 'en',
                'pushMethod': 'local', 'cardType': 'long-study'})
    json.dump(cfg, open(os.path.join(bd, 'config.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)

    items = []
    for i in range(1, a.cards + 1):
        items.append({
            'id': 'c-%02d' % i, 'idx': i, 'chapter': '示例章',
            'topic': 'Sample topic %d' % i,
            'coreIdea': 'Core idea %d — kept local by default.' % i,
            'explanation': 'Block A %d\n\nBlock B %d' % (i, i),
            'quote': 'Quote %d' % i,
            'points': ['Point %d.1' % i, 'Point %d.2' % i],
            'terminology': ['Gateway'],
            'relatedLinks': [{'text': 'Docs', 'href': 'https://example.com/%d' % i}],
            'link': 'https://example.com/%d' % i,
        })
    json.dump(items, open(os.path.join(bd, 'items.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)

    json.dump({'bookTitle': cfg['bookTitle'], 'totalCards': len(items),
               'items': ['card_%s.html' % it['id'] for it in items]},
              open(os.path.join(bd, 'index.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)
    json.dump({'lastPushedId': None, 'pushHistory': []},
              open(os.path.join(bd, 'progress.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)

    print(json.dumps({'ok': True, 'dir': bd, 'cards': len(items)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
