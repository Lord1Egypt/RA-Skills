#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate.py — 内容源与译文的一致性校验（推送前必跑）

两类校验：
  1) 全局（--slug）：items 布局/唯一性/数量、index.json 是否存在且与内容源
     **同步（含顺序）**、必填字段、index.json 里引用的卡片是否都能在内容源里找到。
  2) 逐卡（--slug + --payload + --zh）：中英**逐块对齐**（块数必须一致，
     否则 PDF 里的中英对照会错位）、术语覆盖、关键字段是否漏译。

用法：
    python validate.py --slug <slug>
    python validate.py --slug <slug> --payload p.json --zh z.json
    python validate.py --slug <slug> --payload p.json --zh z.json --strict

退出码：0 通过；1 有 error（--strict 时 warning 也算失败）。
"""
import argparse
import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.environ.get('B2L_DATA_DIR') or os.path.join(SKILL_DIR, 'books')

sys.path.insert(0, SKILL_DIR)
import items_io  # noqa: E402


def split_blocks(text):
    out, cur = [], []
    for line in (text or '').split('\n'):
        if line.strip() == '':
            if cur:
                out.append('\n'.join(cur))
                cur = []
        else:
            cur.append(line)
    if cur:
        out.append('\n'.join(cur))
    return [b for b in out if b.strip()]


def check_global(bd, errors, warnings):
    layout = items_io.describe_layout(bd)
    if layout == 'missing':
        errors.append('内容源缺失：既没有 items.json 也没有 items/index.json')
        return None
    if layout == 'conflict':
        errors.append('items.json 与 items/ 分章节布局**并存**（读取按 split 优先）。'
                      '请删除旧的 items.json，避免误改旧文件')
    items = items_io.load_items(bd)
    dups = items_io.check_unique_ids(items)
    if dups:
        errors.append('id 重复（会导致卡片互相覆盖）：%s' % ', '.join(map(str, dups)))
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            errors.append('第 %d 个 item 不是对象（是 %s）：内容源结构损坏'
                          % (i + 1, type(it).__name__))
            continue
        if not it.get('id'):
            errors.append('第 %d 个 item 缺少 id' % (i + 1))
        if not it.get('topic'):
            warnings.append('item %s 缺少 topic（卡片标题会空）' % it.get('id'))
    idx_path = os.path.join(bd, 'index.json')
    if not os.path.exists(idx_path):
        # 最常见的失误（漏跑 gen-index）必须拦下，静默放行会让推送读旧索引
        errors.append('index.json 不存在：先运行 book_setup.py gen-index <slug>')
        return items
    index = json.load(open(idx_path, encoding='utf-8'))
    total = index.get('totalCards', 0) or 0
    if total != len(items):
        errors.append('index.json totalCards=%s 与内容源条数 %d 不一致（需重跑 gen-index）'
                      % (total, len(items)))
    ids = {it.get('id') for it in items if isinstance(it, dict)}
    missing = []
    for fn in index.get('items', []):
        cid = fn[len('card_'):-len('.html')] if fn.startswith('card_') and fn.endswith('.html') else None
        if cid and cid not in ids:
            missing.append(cid)
    if missing:
        errors.append('index.json 引用了内容源中不存在的卡片：%s（需重跑 gen-index）'
                      % ', '.join(missing[:10]))
    # 顺序校验：get_next_index 完全按 index['items'] 顺序取卡，
    # 内容源重排但没重跑 gen-index 时，推送顺序会被打乱/跳卡
    expected = ['card_%s.html' % it.get('id')
                for it in items if isinstance(it, dict) and it.get('id')]
    if index.get('items') != expected:
        errors.append('index.json 顺序与内容源不一致（内容源重排过？需重跑 gen-index）')
    return items


def check_pair(payload, zh, errors, warnings):
    language = payload.get('language', 'en')
    if language != 'en':
        warnings.append('language=%s，跳过中英对照校验' % language)
        return
    en_blocks = split_blocks(payload.get('explanation', ''))
    zh_blocks = split_blocks((zh or {}).get('explanationZh', ''))
    if len(en_blocks) != len(zh_blocks):
        errors.append('正文块数不对齐：英文 %d 段 / 中文 %d 段（PDF 中英对照会错位）'
                      % (len(en_blocks), len(zh_blocks)))
    for key, zh_key in (('topic', 'topicZh'), ('coreIdea', 'coreIdeaZh'),
                        ('quote', 'quoteZh')):
        if payload.get(key) and not (zh or {}).get(zh_key):
            warnings.append('漏译：%s 有内容但 %s 为空' % (key, zh_key))
    terms = payload.get('terminology') or []
    tzh = (zh or {}).get('terminologyZh')
    if tzh is None:
        tzh = {}
    if not isinstance(tzh, dict):
        errors.append('terminologyZh 必须是 {英文: 中文} 对象（收到 %s）'
                      % type(tzh).__name__)
        return
    if terms and not tzh:
        warnings.append('术语未核对：terminology 非空但 terminologyZh 为空')
    else:
        miss = [t for t in terms if isinstance(t, str) and t not in tzh]
        if miss:
            warnings.append('以下术语未给出中文译名：%s' % ', '.join(miss[:8]))
    if payload.get('points') and not (zh or {}).get('pointsZh'):
        warnings.append('漏译：points 非空但 pointsZh 为空（长图会退回显示原文）')


def main():
    ap = argparse.ArgumentParser(description='内容源与译文一致性校验')
    ap.add_argument('--slug', required=True)
    ap.add_argument('--payload')
    ap.add_argument('--zh')
    ap.add_argument('--strict', action='store_true', help='warning 也视为失败')
    a = ap.parse_args()

    bd = os.path.join(BOOKS_DIR, a.slug)
    errors, warnings = [], []
    items = None
    try:
        items = check_global(bd, errors, warnings)

        if a.payload:
            try:
                payload = json.load(open(a.payload, encoding='utf-8'))
            except (OSError, ValueError) as e:
                errors.append('载荷文件读取失败 %s: %s' % (a.payload, e))
                payload = None
            zh = {}
            if a.zh:
                try:
                    zh = json.load(open(a.zh, encoding='utf-8'))
                except (OSError, ValueError) as e:
                    errors.append('翻译文件读取失败 %s: %s' % (a.zh, e))
                    zh = None
            if payload is not None and zh is not None:
                check_pair(payload, zh, errors, warnings)
                if items:
                    cid = payload.get('nextId')
                    if cid and not items_io.find_item(items, cid):
                        errors.append('载荷里的 nextId=%s 不在内容源中' % cid)
    except Exception as e:  # 任何未预期异常都以 JSON 报出，保持输出可解析
        errors.append('校验过程异常：%s: %s' % (type(e).__name__, e))

    result = {'ok': not errors and not (a.strict and warnings),
              'slug': a.slug, 'layout': items_io.describe_layout(bd),
              'items': len(items) if items else 0,
              'errors': errors, 'warnings': warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result['ok'] else 1)


if __name__ == '__main__':
    main()
