#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""items_io.py — items 内容源读写（兼容单文件与分章节两种布局）

为什么需要：内容多的时候，把几百张卡片塞进一个 `items.json` 很难编辑，
也不利于并行分工。本模块让上层代码对布局**无感知**：

    单文件布局（默认，兼容旧版）
        books/<slug>/items.json
    分章节布局（内容多时推荐）
        books/<slug>/items/index.json          {"chapters":[{"file":"ch01.json","title":"…"}]}
        books/<slug>/items/ch01.json           [ {item}, {item} … ]

注意：这里的 index.json 是**内容源索引**，和推送用的 `books/<slug>/index.json`
（卡片顺序 / 总数）不是同一个文件。

**双布局并存**（single→split 迁移后旧 items.json 未删）：读取按 **split** 优先
（迁移方向），`describe_layout` 返回 'conflict' 供诊断（validate.py 会报错，
提示删除旧的 items.json）。

对外接口：
    load_items(book_dir)          → [item, …]（顺序 = 卡片顺序）
    items_id_map(items)           → {id: item}
    find_item(items, item_id)     → item | None
    describe_layout(book_dir)     → 'single' | 'split' | 'conflict' | 'missing'
    mutate_items(book_dir, fn)    → 就地修改所有 item 并按原布局原子写回
    split_writer(book_dir, chapters) → 写分章节布局（原子 + 清理废弃章节文件）
"""
import json
import os
import tempfile


def _read_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _atomic_json(path, obj):
    """原子写 JSON：先写临时文件再 os.replace，中途被杀不会留下截断文件。"""
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix='.tmp_', dir=d)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except Exception:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def _as_list(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get('items') or []
    return []


def _effective_layout(book_dir):
    """读取用布局：split 优先（迁移方向），再 single。"""
    if os.path.exists(os.path.join(book_dir, 'items', 'index.json')):
        return 'split'
    if os.path.exists(os.path.join(book_dir, 'items.json')):
        return 'single'
    return 'missing'


def describe_layout(book_dir):
    """诊断用布局描述。两种布局并存时返回 'conflict'。"""
    has_single = os.path.exists(os.path.join(book_dir, 'items.json'))
    has_split = os.path.exists(os.path.join(book_dir, 'items', 'index.json'))
    if has_single and has_split:
        return 'conflict'
    if has_split:
        return 'split'
    if has_single:
        return 'single'
    return 'missing'


def load_items(book_dir):
    """读取全部 item（两种布局通吃），返回按卡片顺序排列的列表。

    双布局并存时按 **split**（迁移目标）读取；describe_layout/validate 会提示
    清理旧 items.json，避免下次误改。
    """
    layout = _effective_layout(book_dir)
    if layout == 'single':
        return _as_list(_read_json(os.path.join(book_dir, 'items.json')))

    if layout == 'split':
        meta = _read_json(os.path.join(book_dir, 'items', 'index.json'))
        out = []
        for ch in meta.get('chapters', []):
            fn = ch.get('file')
            if not fn:
                continue
            part = os.path.join(book_dir, 'items', fn)
            if not os.path.exists(part):
                raise FileNotFoundError('章节文件不存在: %s（检查 items/index.json）' % part)
            out.extend(_as_list(_read_json(part)))
        return out

    raise FileNotFoundError(
        '找不到 %s/items.json 或 %s/items/index.json' % (book_dir, book_dir))


def items_id_map(items):
    return {it.get('id'): it for it in items if isinstance(it, dict)}


def find_item(items, item_id):
    for it in items:
        if isinstance(it, dict) and it.get('id') == item_id:
            return it
    return None


def check_unique_ids(items):
    """返回重复 id 列表（空列表表示没问题）。非 dict 元素跳过（由上层校验报错）。"""
    seen, dups = set(), []
    for it in items:
        if not isinstance(it, dict):
            continue
        i = it.get('id')
        if i in seen and i not in dups:
            dups.append(i)
        seen.add(i)
    return dups


def mutate_items(book_dir, fn):
    """就地修改所有 item（两种布局通吃），写回时**保持原布局**并原子落盘。

    fn: callable(item_dict) -> None（直接改传入的 dict）。
    典型用途：download-imgs 把 image 字段替换为 data URI。
    """
    layout = _effective_layout(book_dir)
    if layout == 'single':
        path = os.path.join(book_dir, 'items.json')
        items = _as_list(_read_json(path))
        for it in items:
            if isinstance(it, dict):
                fn(it)
        _atomic_json(path, items)
        return

    if layout == 'split':
        d = os.path.join(book_dir, 'items')
        idx_path = os.path.join(d, 'index.json')
        meta = _read_json(idx_path)
        for ch in meta.get('chapters', []):
            fp = os.path.join(d, ch.get('file') or '')
            if not ch.get('file') or not os.path.exists(fp):
                continue
            part = _as_list(_read_json(fp))
            for it in part:
                if isinstance(it, dict):
                    fn(it)
            _atomic_json(fp, part)
        _atomic_json(idx_path, meta)
        return

    raise FileNotFoundError(
        '找不到内容源（%s/items.json 或 items/index.json），无法写回' % book_dir)


def split_writer(book_dir, chapters):
    """把内容写成分章节布局（原子写 + 清理废弃章节文件）。

    chapters: [{'file': 'ch01.json', 'title': '第一章', 'items': [ ... ]}, …]
    """
    d = os.path.join(book_dir, 'items')
    os.makedirs(d, exist_ok=True)
    # 先记下旧章节清单（用于清理废弃文件），再写新内容
    idx_path = os.path.join(d, 'index.json')
    old_files = set()
    if os.path.exists(idx_path):
        try:
            old_files = {ch.get('file') for ch in _read_json(idx_path).get('chapters', [])
                         if ch.get('file')}
        except Exception:
            old_files = set()
    index = {'chapters': []}
    keep_files = set()
    for ch in chapters:
        keep_files.add(ch['file'])
        _atomic_json(os.path.join(d, ch['file']), ch['items'])
        index['chapters'].append({'file': ch['file'], 'title': ch.get('title', '')})
    # 清理上一轮登记过、本次已不存在的章节文件（避免 load_items 读到陈旧数据）
    for old in (old_files - keep_files):
        try:
            os.remove(os.path.join(d, old))
        except OSError:
            pass
    _atomic_json(idx_path, index)
    return idx_path
