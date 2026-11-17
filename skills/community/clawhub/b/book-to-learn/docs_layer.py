#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docs_layer.py — 操作指南 + 进度笔记（本地文件为底，IMA 可选镜像）

为什么需要：这类「拆解 + 分批推送」的任务周期很长，期间会话记忆会被压缩、
可能换设备、换 agent。只要把**操作指南**和**进度笔记**落到持久化目录，
任何人（或任何 agent）读这两份文件就能立刻恢复全部上下文。

设计：
  * **本地文件为底**：books/<slug>/docs/guide.md、books/<slug>/docs/progress.md
    —— 不依赖任何平台，任何环境都能用。
  * **IMA 是可选镜像**：`notes.channel` 为 ima/both 且环境里有 IMA 凭据时，
    调用 IMA OpenAPI 新建/追加同名笔记（凭据走环境变量，不落盘）。

用法：
    python docs_layer.py init   --slug X --title "书名/站点名"      # 生成两份文档骨架
    python docs_layer.py refresh --slug X                            # 按 config/catalog 刷新指南
    python docs_layer.py log    --slug X --entry "10，已推送，序号OC010。"
    python docs_layer.py status --slug X                             # 打印进度（最新更新记录）
    python docs_layer.py mirror --slug X                             # 可选：镜像到 IMA 笔记
"""
import argparse
import datetime
import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
# 数据根目录：默认在 skill 目录下的 books/；可用环境变量 B2L_DATA_DIR 改到持久化工作目录
BOOKS_DIR = os.environ.get('B2L_DATA_DIR') or os.path.join(SKILL_DIR, 'books')
sys.path.insert(0, SKILL_DIR)

TODAY = datetime.date.today().isoformat()


def load_json(p, default=None):
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    return default


def docs_dir(slug, cfg=None):
    cfg = cfg or {}
    d = ((cfg.get('notes') or {}).get('dir') or '').strip()
    if not d:
        return os.path.join(BOOKS_DIR, slug, 'docs')
    if not os.path.isabs(d):
        # 相对路径按书数据目录解析（进程 CWD 不可依赖）
        d = os.path.join(BOOKS_DIR, slug, d)
    return d


def section_summary(catalog, cfg):
    """按 catalog 的 section 聚合卡片数。"""
    cfg = cfg or {}
    zh = {}
    chapters = cfg.get('chapters') or []
    for c in chapters:
        zh[c.get('name')] = c.get('zh')
    if (cfg.get('source') or {}).get('site', {}).get('sections'):
        for c in cfg['source']['site']['sections']:
            zh[c.get('name')] = c.get('zh')
    counts = {}
    for it in catalog or []:
        s = it.get('section') or '—'
        counts[s] = counts.get(s, 0) + 1
    parts = ['%s %s=%d' % (s, zh.get(s) or '', n) for s, n in counts.items()]
    return ' ｜ '.join(parts) if parts else '（待核定）'


def render_progress(slug, title, catalog, cfg, records):
    rows = ['| 一级类目 | 项目 | 链接 | 录入序号 |', '|---|---|---|---|']
    for it in catalog or []:
        rows.append('| %s | %s | %s | 无 |' % (it.get('section', ''), it.get('title', ''),
                                               it.get('url', '')))
    body = '\n'.join(rows) if catalog else '（清单待核定）'
    rec = '\n'.join(records) if records else '（尚未推送）'
    return ('# 【%s·学习卡片·进度】\n\n'
            '> 本笔记记录推送进度。**进度以最底部「更新记录」最新一段为准**。\n'
            '> 全量清单共 **%d** 张（%s）。\n'
            '> 维护约定：更新记录**只增不删**，最新在最底部。\n\n'
            '## 一、全量清单\n\n%s\n\n'
            '## 二、更新记录（只增不删，最新在最底部）\n\n%s\n'
            % (title, len(catalog or []), section_summary(catalog, cfg), body, rec))


def render_guide(slug, title, catalog, cfg, records):
    ima = cfg.get('ima') or {}
    naming = cfg.get('naming') or {}
    src = cfg.get('source') or {}
    renderer = cfg.get('renderer') or {}
    return ('# 【%s·学习卡片·操作指南】\n\n'
            '用途：会话记忆被压缩 / 换设备 / 换 agent 后，读本文件即可恢复本任务上下文。\n'
            '任何操作前先读本文件，再按其中路径查数据。\n'
            '最后更新：%s\n\n'
            '## 0. 一句话任务\n\n'
            '把来源拆成学习卡片（一次性拆解、分批推送）。每张产出：原文长图 + 对照文档。\n\n'
            '## 1. 范围与总数\n\n'
            '- 来源类型：%s\n- 站点/文件：%s\n- 卡片总数：%d（%s）\n\n'
            '## 2. 工作目录\n\n'
            '- 数据目录：`books/%s/`\n'
            '- 清单 `catalog.json`｜内容源 `items.json`（或 `items/` 分章节）｜进度 `progress.json`\n'
            '- 原始抓取 `raw/pages/`、`raw/imgs/`｜产物 `cards/`｜文档 `docs/`\n\n'
            '## 3. 进度查看位置\n\n'
            '- 主：`docs/progress.md` 底部「更新记录」最新一段\n'
            '- 辅：`progress.json`（`push_card.py status --book %s`）\n\n'
            '## 4. 命名与编号规则\n\n'
            '- 文件名：`%s`\n- 卡片内标记：`%s`\n'
            '- **双轨**：文件名用推送序号（连续）；卡片标记与笔记录入用清单绝对序号（跳过会跳号）\n\n'
            '## 5. 推送 SOP\n\n'
            '1. `push_card.py next --book %s [--n N]` 取下一张（或批量取 N 张）\n'
            '2. 联网核对术语并实时翻译 → 写翻译 JSON\n'
            '3. `render.py --type %s --payload P --zh Z --out O` 生成产物\n'
            '4. 按 pushMethod 推送（本地/IMA/飞书）\n'
            '5. 成功后 `push_card.py mark --book %s <id> success`\n'
            '6. **推完必须列出「接下来 N 张」**，供用户决定跳过\n\n'
            '## 6. 渠道与目标\n\n'
            '- pushMethod：%s\n- IMA：kbName=%s / folderName=%s\n'
            '- 凭据一律走环境变量，不写进 config\n\n'
            '## 7. 渲染规则\n\n'
            '- 卡片类型：%s；引擎映射：%s\n'
            '- 超链接一律纯文本（知识库/IM 不可点击）\n'
            '- 破折号兜底 + 字体自动探测见 `render_common.py`\n\n'
            '## 8. 注意事项\n\n'
            '- 首次使用必须先与用户确认配置（`config.confirmed`），确认前不要开始拆解\n'
            '- 推送成功才记进度；失败必须通知\n'
            '- 详见 `references/pitfalls.md`\n\n'
            '## 9. 变更记录\n\n%s\n'
            % (title, TODAY, src.get('type', 'book'),
               src.get('url') or src.get('file') or '', len(catalog or []),
               section_summary(catalog, cfg), slug, slug,
               naming.get('fileTemplate', '{prefix}{seq:03d} {sectionZh}——{chainZh}'),
               naming.get('markerTemplate', '{idx}/{total}'), slug,
               cfg.get('cardType', 'pdf-standard'), slug,
               cfg.get('pushMethod', 'local'), ima.get('kbName', ''), ima.get('folderName', ''),
               cfg.get('cardType', 'pdf-standard'),
               ', '.join('%s→%s' % (k, v) for k, v in renderer.items()) or '（默认）',
               '\n'.join(records) if records else '（无）'))


def cmd_init(a):
    bd = os.path.join(BOOKS_DIR, a.slug)
    cfg = load_json(os.path.join(bd, 'config.json'), {}) or {}
    catalog = load_json(os.path.join(bd, 'catalog.json'), []) or []
    title = a.title or cfg.get('bookTitle') or a.slug
    d = docs_dir(a.slug, cfg)
    os.makedirs(d, exist_ok=True)
    gp, pp = os.path.join(d, 'guide.md'), os.path.join(d, 'progress.md')
    if not os.path.exists(gp) or a.force:
        open(gp, 'w', encoding='utf-8').write(render_guide(a.slug, title, catalog, cfg, []))
    if not os.path.exists(pp) or a.force:
        if os.path.exists(pp):
            import shutil
            shutil.copy2(pp, pp + '.bak')  # 覆写前备份，防标记失配导致历史丢失
        open(pp, 'w', encoding='utf-8').write(render_progress(a.slug, title, catalog, cfg, []))
    print(json.dumps({'ok': True, 'guide': gp, 'progress': pp, 'channel':
                      (cfg.get('notes') or {}).get('channel', 'local')}, ensure_ascii=False))


def cmd_refresh(a):
    bd = os.path.join(BOOKS_DIR, a.slug)
    cfg = load_json(os.path.join(bd, 'config.json'), {}) or {}
    catalog = load_json(os.path.join(bd, 'catalog.json'), []) or []
    title = cfg.get('bookTitle') or a.slug
    d = docs_dir(a.slug, cfg)
    os.makedirs(d, exist_ok=True)
    records = read_records(os.path.join(d, 'progress.md'))
    open(os.path.join(d, 'guide.md'), 'w', encoding='utf-8').write(
        render_guide(a.slug, title, catalog, cfg, records))
    open(os.path.join(d, 'progress.md'), 'w', encoding='utf-8').write(
        render_progress(a.slug, title, catalog, cfg, records))
    print(json.dumps({'ok': True, 'dir': d, 'records': len(records)}, ensure_ascii=False))


def read_records(progress_path):
    """从 progress.md 底部「更新记录」段落读回记录行（只增不删）。"""
    if not os.path.exists(progress_path):
        return []
    txt = open(progress_path, encoding='utf-8').read()
    if '## 二、更新记录' not in txt:
        return []
    tail = txt.split('## 二、更新记录', 1)[1]
    out = []
    for line in tail.split('\n'):
        s = line.strip()
        # 跳过空行、标题行、以及「（尚未推送）/（无）/（只增不删…）」这类占位说明
        if not s or s.startswith('#') or s.startswith('（'):
            continue
        out.append(s)
    return out


def cmd_log(a):
    bd = os.path.join(BOOKS_DIR, a.slug)
    cfg = load_json(os.path.join(bd, 'config.json'), {}) or {}
    d = docs_dir(a.slug, cfg)
    pp = os.path.join(d, 'progress.md')
    if not os.path.exists(pp):
        print(json.dumps({'ok': False, 'error': 'progress.md 不存在，先跑 init'}, ensure_ascii=False))
        sys.exit(1)
    with open(pp, 'a', encoding='utf-8') as f:
        f.write(a.entry.rstrip() + '\n')
    print(json.dumps({'ok': True, 'appended': a.entry.rstrip(),
                      'progress': pp, 'latest': a.entry.rstrip()}, ensure_ascii=False))


def cmd_status(a):
    bd = os.path.join(BOOKS_DIR, a.slug)
    cfg = load_json(os.path.join(bd, 'config.json'), {}) or {}
    d = docs_dir(a.slug, cfg)
    recs = read_records(os.path.join(d, 'progress.md'))
    print(json.dumps({'ok': True, 'records': len(recs),
                      'latest': recs[-1] if recs else None}, ensure_ascii=False))


def cmd_mirror(a):
    """可选：把本地两份文档推到 IMA 笔记（需要 IMA 凭据）。"""
    import urllib.request
    bd = os.path.join(BOOKS_DIR, a.slug)
    cfg = load_json(os.path.join(bd, 'config.json'), {}) or {}
    notes = cfg.get('notes') or {}
    if notes.get('channel', 'local') == 'local':
        print(json.dumps({'ok': True, 'skipped': 'notes.channel=local（只写本地文件）'},
                         ensure_ascii=False))
        return
    cid, key = os.environ.get('IMA_OPENAPI_CLIENTID'), os.environ.get('IMA_OPENAPI_APIKEY')
    if not cid or not key:
        print(json.dumps({'ok': False, 'error': 'IMA 凭据缺失（IMA_OPENAPI_CLIENTID / '
                          'IMA_OPENAPI_APIKEY），本地文件不受影响'}, ensure_ascii=False))
        sys.exit(1)
    d = docs_dir(a.slug, cfg)
    out = {}
    for name, key_path in (('guide', 'guideNoteId'), ('progress', 'progressNoteId')):
        p = os.path.join(d, '%s.md' % name)
        if not os.path.exists(p):
            continue
        content = open(p, encoding='utf-8').read()
        nid = (notes.get('ima') or {}).get(key_path) or ''
        body = json.dumps({'note_id': nid, 'content': content}).encode()
        req = urllib.request.Request(
            'https://ima.qq.com/openapi/note/v1/push_note', data=body, method='POST',
            headers={'Content-Type': 'application/json', 'ima-openapi-clientid': cid,
                     'ima-openapi-apikey': key})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=60))
            out[name] = r.get('code')
        except Exception as e:
            out[name] = 'ERR:%s' % e
    ok = all(not str(v).startswith('ERR') for v in out.values()) if out else True
    print(json.dumps({'ok': ok, 'ima': out}, ensure_ascii=False))
    if not ok:
        sys.exit(1)  # 镜像失败要能被自动化感知


def main():
    ap = argparse.ArgumentParser(description='操作指南 + 进度笔记（本地为底，IMA 可选）')
    sub = ap.add_subparsers(dest='cmd')
    p1 = sub.add_parser('init'); p1.add_argument('--slug', required=True)
    p1.add_argument('--title'); p1.add_argument('--force', action='store_true')
    p2 = sub.add_parser('refresh'); p2.add_argument('--slug', required=True)
    p3 = sub.add_parser('log'); p3.add_argument('--slug', required=True)
    p3.add_argument('--entry', required=True)
    p4 = sub.add_parser('status'); p4.add_argument('--slug', required=True)
    p5 = sub.add_parser('mirror'); p5.add_argument('--slug', required=True)
    a = ap.parse_args()
    if a.cmd == 'init':
        cmd_init(a)
    elif a.cmd == 'refresh':
        cmd_refresh(a)
    elif a.cmd == 'log':
        cmd_log(a)
    elif a.cmd == 'status':
        cmd_status(a)
    elif a.cmd == 'mirror':
        cmd_mirror(a)
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
