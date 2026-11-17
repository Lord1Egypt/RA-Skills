#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_fixes.py — v1.6.1 修复回归测试（离线，无网络依赖）。

覆盖：normalize_quotes 代码/URL 保护、items_io 双布局与原子性、
fetch_site 的 sitemapindex 展开 / include 边界 / safe_slug、
push_card 的 id 校验与 mark 顺序回写、gen_card_long 术语字符串列表。
运行：python3 tests/test_fixes.py   （输出 JSON，全过 ok=true）
"""
import json
import os
import shutil
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

CHECKS = []


def check(name, fn):
    try:
        fn()
        CHECKS.append({'check': name, 'ok': True})
    except Exception as e:
        CHECKS.append({'check': name, 'ok': False, 'error': '%s: %s' % (type(e).__name__, e)})


# ---------------------------------------------------------------- normalize_quotes
def t_nq_inline_code():
    import normalize_quotes as nq
    out = nq.normalize_chinese_text_only('调用 `print("你好")` 输出"结果"')
    assert '`print("你好")`' in out, out
    assert '\u201c结果\u201d' in out, out


def t_nq_fenced():
    import normalize_quotes as nq
    out = nq.normalize_chinese_text_only('```\nprint("hi")\n```\n这是"示例"')
    assert 'print("hi")' in out, out


def t_nq_url():
    import normalize_quotes as nq
    out = nq.normalize_chinese_text_only('访问 https://a.com/s?q="数据" 查看"结果"')
    assert 'https://a.com/s?q="数据"' in out, out
    assert '\u201c结果\u201d' in out, out


def t_nq_default_smart():
    import normalize_quotes as nq
    d = {'text': '哈希表是"key-value"结构，"键"是核心'}
    nq.normalize_dict_quotes(d, ['text'])  # 默认 smart=True
    assert '"key-value"' in d['text'], d['text']
    assert '\u201c键\u201d' in d['text'], d['text']


def t_nq_inch_mark():
    import normalize_quotes as nq
    out = nq.normalize_chinese_text_only('屏幕 27" 对角线，他说"好"')
    assert '27"' in out, out
    assert '\u201c好\u201d' in out, out


def t_nq_list_fields():
    import normalize_quotes as nq
    zh = {'pointsZh': ['第一"点"'],
          'relatedLinksZh': [{'href': 'https://a.com', 'textZh': '带"引号"标题'}]}
    nq.normalize_all(zh, None, 'en', smart=True)
    assert zh['pointsZh'][0] == '第一\u201c点\u201d'
    assert zh['relatedLinksZh'][0]['textZh'] == '带\u201c引号\u201d标题'


# ---------------------------------------------------------------- items_io
def _mk_book(bd, single=True):
    os.makedirs(bd, exist_ok=True)
    if single:
        with open(os.path.join(bd, 'items.json'), 'w', encoding='utf-8') as f:
            json.dump([{'id': 'c1', 'topic': 'A'}, {'id': 'c2', 'topic': 'B'}], f)
    else:
        d = os.path.join(bd, 'items')
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'ch01.json'), 'w', encoding='utf-8') as f:
            json.dump([{'id': 'c1', 'topic': 'A'}], f)
        with open(os.path.join(d, 'index.json'), 'w', encoding='utf-8') as f:
            json.dump({'chapters': [{'file': 'ch01.json', 'title': '一'}]}, f)


def t_items_conflict():
    import items_io
    bd = tempfile.mkdtemp()
    try:
        _mk_book(bd, single=True)
        _mk_book(bd, single=False)  # 再写 split → 并存
        assert items_io.describe_layout(bd) == 'conflict'
        items = items_io.load_items(bd)  # conflict 按 split 读取
        assert [i['id'] for i in items] == ['c1'], items
    finally:
        shutil.rmtree(bd)


def t_items_mutate_split():
    import items_io
    bd = tempfile.mkdtemp()
    try:
        _mk_book(bd, single=False)
        items_io.mutate_items(bd, lambda it: it.update(image='data:image/png;base64,x'))
        items = items_io.load_items(bd)
        assert items[0]['image'] == 'data:image/png;base64,x'
        # 单文件布局未被动过
        assert not os.path.exists(os.path.join(bd, 'items.json'))
    finally:
        shutil.rmtree(bd)


def t_items_str_elem_no_crash():
    import items_io
    dups = items_io.check_unique_ids([{'id': 'a'}, 'oops', {'id': 'a'}])
    assert dups == ['a'], dups


def t_items_split_writer_cleans_stale():
    import items_io
    bd = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(bd, 'items'), exist_ok=True)
        stale = os.path.join(bd, 'items', 'ch09.json')
        with open(stale, 'w', encoding='utf-8') as f:
            json.dump([{'id': 'z'}], f)
        with open(os.path.join(bd, 'items', 'index.json'), 'w', encoding='utf-8') as f:
            json.dump({'chapters': [{'file': 'ch09.json', 'title': '旧'}]}, f)
        items_io.split_writer(bd, [{'file': 'ch01.json', 'title': '新', 'items': [{'id': 'c1'}]}])
        assert not os.path.exists(stale), '废弃章节文件未清理'
        assert items_io.load_items(bd)[0]['id'] == 'c1'
    finally:
        shutil.rmtree(bd)


# ---------------------------------------------------------------- fetch_site
def t_fetch_sitemapindex():
    import fetch_site as fs
    idx_xml = ('<sitemapindex><sitemap><loc>https://e.com/sm.xml</loc></sitemap></sitemapindex>')
    sub_xml = '<urlset><url><loc>https://e.com/a</loc></url><url><loc>https://e.com/b</loc></url></urlset>'
    orig = fs.http_get
    try:
        fs.http_get = lambda u, timeout=20, binary=False: (sub_xml if 'sm.xml' in u else idx_xml)
        urls, src = fs.fetch_sitemap('https://e.com', 'auto', 5)
        assert urls == ['https://e.com/a', 'https://e.com/b'], urls
    finally:
        fs.http_get = orig


def t_fetch_include_boundary():
    import fetch_site as fs
    assert fs.keep('https://e.com/startups', 'https://e.com', ['/start'], []) is False
    assert fs.keep('https://e.com/start/x', 'https://e.com', ['/start'], []) is True


def t_fetch_safe_slug():
    import fetch_site as fs
    assert fs.safe_slug('/Help:Contents') == 'Help_Contents'
    assert fs.safe_slug('/a/b') == 'a_b'
    assert fs.safe_slug('/') == 'index'


# ---------------------------------------------------------------- push_card
def t_push_mark_rejects_bad_id():
    import push_card as pc
    bd = tempfile.mkdtemp()
    pc.BOOKS_DIR = bd          # 隔离：mark 用 book_dir('x') = bd/x
    try:
        os.makedirs(os.path.join(bd, 'x'), exist_ok=True)
        bd = os.path.join(bd, 'x')
        with open(os.path.join(bd, 'index.json'), 'w', encoding='utf-8') as f:
            json.dump({'items': ['card_c1.html', 'card_c2.html'], 'totalCards': 2}, f)
        with open(os.path.join(bd, 'progress.json'), 'w', encoding='utf-8') as f:
            json.dump({'lastPushedId': None, 'pushHistory': []}, f)

        import contextlib, io as _io
        class A:
            book = 'x'
            ids = None
            id = ['card_c1.html']   # 误传文件名
            status = 'success'
        try:
            with contextlib.redirect_stdout(_io.StringIO()):
                pc.cmd_mark(A())
            raise AssertionError('误传文件名应被拒绝')
        except SystemExit as e:
            assert e.code == 1, e.code
    finally:
        shutil.rmtree(bd)


def t_push_mark_order():
    import push_card as pc
    bd = tempfile.mkdtemp()
    pc.BOOKS_DIR = bd
    try:
        os.makedirs(os.path.join(bd, 'x'), exist_ok=True)
        bd = os.path.join(bd, 'x')
        with open(os.path.join(bd, 'index.json'), 'w', encoding='utf-8') as f:
            json.dump({'items': ['card_a.html', 'card_b.html', 'card_c.html'],
                       'totalCards': 3}, f)
        with open(os.path.join(bd, 'progress.json'), 'w', encoding='utf-8') as f:
            json.dump({'lastPushedId': None, 'pushHistory': []}, f)

        class A:
            book = 'x'
            ids = 'c,a,b'   # 乱序回写
            id = None
            status = 'success'
        import contextlib, io as _io
        with contextlib.redirect_stdout(_io.StringIO()):
            pc.cmd_mark(A())
        progress = json.load(open(os.path.join(bd, 'progress.json'), encoding='utf-8'))
        assert progress['lastPushedId'] == 'c', progress  # 位置最靠后的是 c（index 第 3 个）
    finally:
        shutil.rmtree(bd)


def t_push_stale_progress():
    import push_card as pc
    progress = {'lastPushedId': 'ghost-id'}
    index = {'items': ['card_a.html']}
    try:
        pc.get_next_index(progress, index)
        raise AssertionError('stale 应抛 StaleProgress')
    except pc.StaleProgress:
        pass


# ---------------------------------------------------------------- engines
def t_long_terms_strlist():
    import gen_card_long as g
    payload = {'id': 'x', 'topic': 'T', 'explanation': 'e', 'terminology': ['Gateway', 'Skill']}
    html = g.build_html(payload, None, language='zh')
    assert 'Gateway' in html and 'Skill' in html


def t_bilingual_extra_zh_blocks():
    import gen_card_bilingual as g
    payload = {'topic': 'T', 'explanation': 'One.', 'cardIndex': 1, 'totalCards': 2}
    zh = {'explanationZh': '一。\n\n二。'}
    html = g.build_html(payload, zh, language='en')
    assert '二。' in html, '多出的译文块被丢弃'


def t_normalize_all_chapter_en():
    import normalize_quotes as nq
    payload = {'chapter': '第一章'}
    nq.normalize_all(None, payload, 'en')
    assert payload['chapter'] == '第一章'


def main():
    for name, fn in [
        ('normalize_quotes/行内代码保护', t_nq_inline_code),
        ('normalize_quotes/围栏代码保护', t_nq_fenced),
        ('normalize_quotes/URL保护', t_nq_url),
        ('normalize_quotes/默认smart', t_nq_default_smart),
        ('normalize_quotes/英寸标记', t_nq_inch_mark),
        ('normalize_quotes/列表字段', t_nq_list_fields),
        ('items_io/双布局冲突', t_items_conflict),
        ('items_io/split布局保持回写', t_items_mutate_split),
        ('items_io/非dict容错', t_items_str_elem_no_crash),
        ('items_io/废弃章节清理', t_items_split_writer_cleans_stale),
        ('fetch_site/sitemapindex展开', t_fetch_sitemapindex),
        ('fetch_site/include边界', t_fetch_include_boundary),
        ('fetch_site/safe_slug', t_fetch_safe_slug),
        ('push_card/mark拒绝未知id', t_push_mark_rejects_bad_id),
        ('push_card/mark按index顺序回写', t_push_mark_order),
        ('push_card/stale_progress检测', t_push_stale_progress),
        ('gen_card_long/字符串术语列表', t_long_terms_strlist),
        ('gen_card_bilingual/译文块不丢', t_bilingual_extra_zh_blocks),
        ('normalize_all/en模式chapter', t_normalize_all_chapter_en),
    ]:
        check(name, fn)
    failed = [c for c in CHECKS if not c['ok']]
    print(json.dumps({'ok': not failed, 'total': len(CHECKS), 'failed': len(failed),
                      'checks': CHECKS}, ensure_ascii=False, indent=1))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
