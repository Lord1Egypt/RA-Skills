#!/usr/bin/env python3
"""
Book setup orchestrator for book-to-learn.
Handles the one-time book decomposition: extract → analyze → outline → generate.

This script provides the extraction + scaffolding infrastructure.
The actual AI analysis (chapter detection, knowledge point generation) is
performed by the AI agent following SKILL.md instructions, using these helpers:

  python book_setup.py extract <file> --slug <slug>          Extract text → books/<slug>/full_text.txt
  python book_setup.py init <slug> --title "..." --lang <zh|en>  Create config.json skeleton
  python book_setup.py gen-cards <slug>                      Generate cards/ from items.json
  python book_setup.py gen-index <slug>                      Generate index.json from items.json
  python book_setup.py download-imgs <slug>                  Download images, embed as base64
  python book_setup.py prompt <slug>                         Output the cron prompt for this book

（除 extract 的 --slug 外，slug 传位置参数；也兼容 --slug <slug> 写法）
"""
import json, os, sys, re, base64, hashlib, subprocess, argparse, urllib.request, tempfile

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
# 数据根目录：默认在 skill 目录下的 books/；
# 若本平台 skill 目录不是持久层（容器/沙箱会被重置），用环境变量 B2L_DATA_DIR 指向持久化工作目录。
BOOKS_DIR = os.environ.get('B2L_DATA_DIR') or os.path.join(SKILL_DIR, 'books')

sys.path.insert(0, SKILL_DIR)
import items_io  # noqa: E402  （分章节/单文件两种 items 布局，统一从这里读写）


def _atomic_json(path, obj):
    """原子写 JSON（items.json/index.json 等唯一事实源，中途被杀不留截断文件）。"""
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

def book_dir(slug):
    return os.path.join(BOOKS_DIR, slug)

def ensure_dirs(slug):
    bd = book_dir(slug)
    for d in ['', 'cards', 'images']:
        os.makedirs(os.path.join(bd, d), exist_ok=True)
    return bd

def cmd_extract(args):
    """Extract text from source file → books/<slug>/full_text.txt"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("extract_text", os.path.join(SKILL_DIR, 'extract_text.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    bd = ensure_dirs(args.slug)
    out_path = os.path.join(bd, 'full_text.txt')
    try:
        text = mod.extract(args.file)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(json.dumps({'ok': True, 'out': out_path, 'chars': len(text),
                          'words': len(text.split()), 'slug': args.slug}, ensure_ascii=False))
    except mod.ExtractionError as e:
        print(json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

def cmd_init(args):
    """Create config.json skeleton for a book."""
    bd = ensure_dirs(args.slug)
    cfg_path = os.path.join(bd, 'config.json')
    if os.path.exists(cfg_path) and not args.force:
        print(json.dumps({'ok': False, 'error': 'config.json already exists (use --force to overwrite)'}, ensure_ascii=False))
        sys.exit(1)
    config = {
        'configVersion': 2,
        'bookTitle': args.title or args.slug,
        'bookSlug': args.slug,
        'language': args.lang,
        'pushMethod': 'local',           # 默认零依赖：产物只落本地；IMA/飞书为可选渠道
        'ima': {'kbName': '', 'folderName': ''},
        'feishu': {'webhook': ''},
        'feishuApi': {'appId': '', 'appSecret': '', 'chatId': ''},
        'notifyWebhook': '',
        'granularity': args.granularity,
        'cardPrefix': args.prefix or 'BOOK',
        'template': 'pdf-standard',  # pdf-standard | pdf-large | feishu-card | feishu-card+image
        'cardType': 'pdf-standard',  # 渲染类型 → 引擎映射见 render.py
        'imageFormat': '1:1',  # 1:1 | 1:4 (only for image supplement)
        'testPush': False,  # whether to do a test push after setup
        'createdAt': __import__('datetime').date.today().isoformat(),
        # —— v1.5 新增（全部可选）——
        # 首次使用必须逐项与用户确认；未确认前 push_card.py next 会拒绝发载荷
        'confirmed': {
            'at': '', 'by': '',
            'items': {'source': False, 'language': False, 'cardType': False,
                      'pushMethod': False, 'naming': False, 'notes': False, 'notify': False},
        },
        'source': {'type': 'book', 'file': '', 'bookSource': '',
                   'site': {'url': '', 'sitemap': 'auto', 'include': [], 'exclude': [],
                            'bodySuffix': '.md', 'sections': []}},
        'local': {'outDir': ''},          # pushMethod=local 时的产物输出目录
        'itemsLayout': 'single',           # single | split（内容多时用 items/ 分章节）
        'naming': {'filePrefix': args.prefix or 'BOOK', 'sectionZh': '',
                   'fileTemplate': '{prefix}{seq:03d} {sectionZh}——{chainZh}',
                   'markerTemplate': '{idx}/{total}', 'manifestIndex': False},
        'notes': {'channel': 'local',      # local | ima | both
                  'dir': '',
                  'ima': {'notebookName': '', 'progressNoteId': '', 'guideNoteId': ''}},
        'batch': {'listNextN': 10, 'translateParallel': True},
    }
    _atomic_json(cfg_path, config)
    print(json.dumps({'ok': True, 'config': cfg_path, 'config_content': config}, ensure_ascii=False, indent=2))

def cmd_gen_cards(args):
    """Generate cards/*.html from items.json (preview-only; items.json is the
    single source of truth for push payloads)."""
    bd = book_dir(args.slug)
    items = items_io.load_items(bd)  # 兼容 items.json 与 items/ 分章节两种布局
    if any(not isinstance(it, dict) for it in items):
        print(json.dumps({'ok': False, 'error': 'items 内容源里存在非对象条目，结构损坏'}, ensure_ascii=False))
        sys.exit(1)
    ids = [it.get('id') for it in items]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    if dups:
        print(json.dumps({'ok': False, 'error': 'duplicate ids in items.json (cards would overwrite each other): %s' % ', '.join(map(str, dups))}, ensure_ascii=False))
        sys.exit(1)
    if any(not i for i in ids):
        print(json.dumps({'ok': False, 'error': 'every item needs a non-empty id'}, ensure_ascii=False))
        sys.exit(1)
    cards_dir = os.path.join(bd, 'cards')
    os.makedirs(cards_dir, exist_ok=True)
    # clear old cards
    for f in os.listdir(cards_dir):
        if f.startswith('card_') and f.endswith('.html'):
            os.remove(os.path.join(cards_dir, f))

    CSS = """
:root{--green:#58cc02;--blue:#1cb0f6;--purple:#a560e8;--orange:#ff9600;--red:#ff4b4b;--bg:#eef2f7;--card:#fff;--text:#3c3c3c;--muted:#8a8a8a}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);line-height:1.65;padding:14px}
.card{max-width:480px;margin:0 auto;background:var(--card);border-radius:22px;box-shadow:0 6px 24px rgba(20,40,80,.08);overflow:hidden;border:1px solid #eef0f4}
.card-head{padding:18px 20px 12px}
.progress-row{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.progress-num{font-size:13px;font-weight:700;color:var(--muted);white-space:nowrap}
.progress-bar{flex:1;height:9px;background:#e8ecf2;border-radius:99px;overflow:hidden}
.progress-fill{height:100%;background:linear-gradient(90deg,var(--green),#46a302);border-radius:99px}
.chapter-tag{display:inline-block;font-size:11.5px;font-weight:700;color:#fff;background:linear-gradient(135deg,var(--blue),#0ea5e9);padding:4px 12px;border-radius:99px}
.topic{padding:4px 20px 8px;font-size:22px;font-weight:800;line-height:1.32;color:#1a1a2e}
.section{padding:13px 20px}
.section h3{font-size:11.5px;text-transform:uppercase;letter-spacing:.7px;font-weight:800;margin-bottom:8px;color:#2b2b3a}
.core{background:#eefcf0;border-left:4px solid var(--green);padding:12px 14px;border-radius:0 12px 12px 0;font-size:15px;font-weight:500;color:#234d12}
.expl{font-size:14.5px;color:#444}.expl p{margin-bottom:9px}
.quote{background:#f4efff;border-left:4px solid var(--purple);padding:12px 14px;border-radius:0 12px 12px 0;font-style:italic;font-size:14.5px;color:#5b3b8c}
.app{font-size:14px;color:#444}.app p{margin-bottom:7px;padding-left:18px;position:relative}.app p:before{content:'';position:absolute;left:2px;top:9px;width:6px;height:6px;border-radius:50%;background:var(--orange)}
.terms{display:flex;flex-wrap:wrap;gap:7px}.term{font-size:12.5px;background:#fff7e0;color:#8a5a00;border:1px solid #ffe08a;padding:4px 11px;border-radius:99px}
.img-wrap{padding:6px 20px 4px}.img-wrap img{width:100%;border-radius:14px;border:1px solid #f0f0f0}
.links a{font-size:13px;color:var(--blue);text-decoration:none;word-break:break-all;display:block;margin-bottom:5px}
.translation-panel{margin:14px 20px 20px;padding:18px 16px;background:#f9fafb;border:2px dashed #d7dbe2;border-radius:16px;text-align:center;color:#9ca3af;font-size:14px;min-height:64px;display:flex;align-items:center;justify-content:center}
.src{padding:2px 20px 4px;font-size:11.5px;color:var(--muted);word-break:break-all}
"""
    import html as html_mod
    def esc(s): return html_mod.escape(s or '', quote=True)
    def md_to_html(text):
        return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                      lambda m: '<a href="%s" target="_blank">%s</a>' % (m.group(2), m.group(1)), text or '')
    def paras(text, md=False):
        out = []
        for ln in (text or '').split('\n'):
            ln = ln.strip()
            if ln:
                p = esc(ln)
                if md: p = md_to_html(p)
                out.append('<p>%s</p>' % p)
        return ''.join(out)

    filenames = []
    for i, it in enumerate(items):
        idx = i + 1
        total = len(items)
        pct = round(idx / total * 100)
        p = []
        p.append('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">')
        p.append('<title>%s</title><style>%s</style></head><body>' % (esc(it.get('topic','')), CSS))
        p.append('<div class="card"><div class="card-head"><div class="progress-row"><span class="progress-num">Card %d / %d</span><div class="progress-bar"><div class="progress-fill" style="width:%d%%"></div></div></div><span class="chapter-tag">%s</span></div>' % (idx, total, pct, esc(it.get('chapter',''))))
        p.append('<div class="topic">%s</div>' % esc(it.get('topic','')))
        p.append('<div class="section"><h3>Core Idea</h3><div class="core">%s</div></div>' % esc(it.get('coreIdea','')))
        p.append('<div class="section"><h3>Explanation</h3><div class="expl">%s</div></div>' % paras(it.get('explanation',''), md=True))
        if it.get('quote'):
            p.append('<div class="section"><h3>Key Quote</h3><div class="quote">%s</div></div>' % esc(it['quote']))
        if it.get('application'):
            p.append('<div class="section"><h3>Application</h3><div class="app">%s</div></div>' % paras(it['application'], md=True))
        if it.get('terminology'):
            chips = ''.join('<span class="term">%s</span>' % esc(t) for t in it['terminology'])
            p.append('<div class="section"><h3>Key Terms</h3><div class="terms">%s</div></div>' % chips)
        if it.get('image'):
            p.append('<div class="img-wrap"><img src="%s" alt="figure" loading="lazy"></div>' % esc(it['image']))
        rl = it.get('relatedLinks', [])
        if rl:
            links = ''
            for l in rl:
                href = l.get('href','') if isinstance(l, dict) else str(l)
                text = l.get('text','') if isinstance(l, dict) else ''
                label = text if text else href
                links += '<a href="%s" target="_blank">%s</a>' % (esc(href), esc(label))
            p.append('<div class="section"><h3>Related Links</h3><div class="links">%s</div></div>' % links)
        if it.get('link'):
            p.append('<div class="src">Source: %s</div>' % esc(it['link']))
        p.append('<div class="translation-panel" id="translation-panel"><span>中文翻译将在推送时生成</span></div>')
        p.append('</div></body></html>')
        fn = 'card_%s.html' % it['id']
        with open(os.path.join(cards_dir, fn), 'w', encoding='utf-8') as f:
            f.write(''.join(p))
        filenames.append(fn)
    print(json.dumps({'ok': True, 'cards_generated': len(filenames), 'slug': args.slug}, ensure_ascii=False))

def cmd_gen_index(args):
    """Generate index.json from items.json."""
    bd = book_dir(args.slug)
    items = items_io.load_items(bd)  # 兼容 items.json 与 items/ 分章节两种布局
    if any(not isinstance(it, dict) for it in items):
        print(json.dumps({'ok': False, 'error': 'items 内容源里存在非对象条目，结构损坏'}, ensure_ascii=False))
        sys.exit(1)
    ids = [it.get('id') for it in items]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    if dups:
        print(json.dumps({'ok': False, 'error': 'duplicate ids in items.json: %s' % ', '.join(map(str, dups))}, ensure_ascii=False))
        sys.exit(1)
    if any(not i for i in ids):
        print(json.dumps({'ok': False, 'error': 'every item needs a non-empty id'}, ensure_ascii=False))
        sys.exit(1)
    config = json.load(open(os.path.join(bd, 'config.json'), encoding='utf-8'))
    index = {
        'bookTitle': config.get('bookTitle', args.slug),
        'bookSource': items[0].get('link', '') if items else '',
        'totalCards': len(items),
        'items': ['card_%s.html' % it['id'] for it in items]
    }
    _atomic_json(os.path.join(bd, 'index.json'), index)
    # also init progress.json if not exists
    prog_path = os.path.join(bd, 'progress.json')
    if not os.path.exists(prog_path):
        _atomic_json(prog_path, {'lastPushedId': None, 'lastPushDate': None, 'pushHistory': []})
    # create daily-progress.md if not exists
    dp_path = os.path.join(bd, 'daily-progress.md')
    if not os.path.exists(dp_path):
        title = config.get('bookTitle', args.slug)
        total = len(items)
        with open(dp_path, 'w', encoding='utf-8') as f:
            f.write(f'# {title} — 每日学习进度\n\n')
            f.write(f'> 共 {total} 个知识点 | 每次推送成功后追加一行记录\n\n')
            f.write(f'| 日期 | 序号 | 卡片ID | 主题 | 推送方式 | 状态 |\n')
            f.write(f'|------|------|--------|------|----------|------|\n')
    print(json.dumps({'ok': True, 'totalCards': len(items), 'slug': args.slug, 'dailyProgress': dp_path}, ensure_ascii=False))

def cmd_download_imgs(args):
    """Download images referenced in items.json, embed as base64 data URIs."""
    bd = book_dir(args.slug)
    items = items_io.load_items(bd)  # 兼容两种布局
    if any(not isinstance(it, dict) for it in items):
        print(json.dumps({'ok': False, 'error': 'items 内容源里存在非对象条目，结构损坏'}, ensure_ascii=False))
        sys.exit(1)
    if not any(it.get('image') for it in items):
        print(json.dumps({'ok': True, 'downloaded': 0, 'embedded': 0, 'slug': args.slug,
                          'note': '内容源里没有 image 字段，无需下载'}, ensure_ascii=False))
        return
    img_dir = os.path.join(bd, 'images')
    os.makedirs(img_dir, exist_ok=True)
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
    import shutil
    if not shutil.which('curl'):
        print(json.dumps({'ok': False, 'error': '未找到 curl 命令（download-imgs 依赖 curl 下载图片）'}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    url_map = {}
    failed = []   # urls we could not fetch after retries
    for it in items:
        u = it.get('image', '') or ''
        if u and not u.startswith('data:') and u not in url_map and u not in failed:
            ext = u.rsplit('.', 1)[-1].split('?')[0].split('-')[0].lower()
            if ext not in ('png','jpg','jpeg','gif','webp','svg'): ext = 'png'
            if ext == 'jpeg': ext = 'jpg'
            h = hashlib.md5(u.encode()).hexdigest()[:10]
            fn = f'img_{h}.{ext}'
            out = os.path.join(img_dir, fn)
            ok = False
            for attempt in range(3):
                # NOTE: no --insecure (TLS is verified); original PDFs may still
                # fail on self-signed hosts, which will be reported in `failed`.
                r = subprocess.run(['curl','-sL','--fail','--max-time','30','-A',UA,'-o',out,u], capture_output=True)
                if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 500:
                    # 魔数校验：SVG 是 XML 文本（<?xml / <svg 开头），其余按二进制魔数
                    head = open(out,'rb').read(256)
                    if (head[:4]==b'\x89PNG' or head[:3]==b'\xff\xd8\xff' or head[:4]==b'GIF8'
                            or head[:4]==b'RIFF'
                            or head[:5]==b'<?xml' or b'<svg' in head[:200]):
                        url_map[u] = fn
                        ok = True
                        break
                if os.path.exists(out) and os.path.getsize(out) <= 500:
                    os.remove(out)
            if not ok:
                failed.append(u)
                if os.path.exists(out):
                    os.remove(out)
    # build data URIs
    data_uris = {}
    for url, fn in url_map.items():
        out = os.path.join(img_dir, fn)
        if os.path.exists(out):
            with open(out, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode('ascii')
            ext = fn.rsplit('.',1)[-1]
            mime = {'png':'image/png','jpg':'image/jpeg','gif':'image/gif','webp':'image/webp','svg':'image/svg+xml'}.get(ext,'image/png')
            data_uris[url] = f'data:{mime};base64,{b64}'
    # update items（布局保持：single → items.json；split → 各章节文件；原子落盘）
    updated = 0
    def _embed(it):
        nonlocal updated
        u = it.get('image', '') or ''
        if u in data_uris:
            it['image'] = data_uris[u]
            updated += 1
    items_io.mutate_items(bd, _embed)
    result = {'ok': True, 'downloaded': len(url_map), 'embedded': updated, 'slug': args.slug}
    if failed:
        result['failed'] = failed
        result['warning'] = ('%d image(s) failed to download after 3 attempts and were left as remote URLs: %s'
                             % (len(failed), '; '.join(failed[:10]) + (' ...' if len(failed) > 10 else '')))
    print(json.dumps(result, ensure_ascii=False))
    if failed:
        # non-fatal, but loud: un-embedded images depend on the remote host at push time
        print('WARNING: some images could not be embedded; they will stay as URLs (offline reading will break for those cards)', file=sys.stderr)

def cmd_summary(args):
    """Print a detailed configuration summary for user confirmation."""
    bd = book_dir(args.slug)
    config = json.load(open(os.path.join(bd, 'config.json'), encoding='utf-8'))
    items = []
    items_path = os.path.join(bd, 'items.json')
    if os.path.exists(items_path):
        items = json.load(open(items_path, encoding='utf-8'))
    progress = {'lastPushedId': None, 'pushHistory': []}
    prog_path = os.path.join(bd, 'progress.json')
    if os.path.exists(prog_path):
        progress = json.load(open(prog_path, encoding='utf-8'))

    template_names = {
        'pdf-standard': 'PDF 标准卡片（长文，多字小字，中英对照）',
        'pdf-large': 'PDF 大字卡片（A4，正文≥18px，标题超大，适合单词/术语）',
        'feishu-card': '飞书交互式卡片（文字排版）',
        'feishu-card+image': '飞书卡片 + 图片补充（1:1或1:4图片随卡片发送）',
    }
    pushed = len(progress.get('pushHistory', []))
    total = len(items)
    has_img = sum(1 for it in items if isinstance(it, dict) and (it.get('image') or '').startswith('data:'))
    has_links = sum(1 for it in items if isinstance(it, dict) and it.get('relatedLinks'))
    has_terms = sum(1 for it in items if isinstance(it, dict) and it.get('terminology'))

    lines = []
    lines.append(f'═══════════════════════════════════════════════════')
    lines.append(f'  《{config.get("bookTitle", args.slug)}》 配置确认')
    lines.append(f'═══════════════════════════════════════════════════')
    lines.append(f'')
    lines.append(f'【基本信息】')
    lines.append(f'  书名：{config.get("bookTitle", "")}')
    lines.append(f'  Slug：{config.get("bookSlug", args.slug)}')
    lines.append(f'  语言：{"中文（无翻译）" if config.get("language")=="zh" else "英文（需联网核对术语+翻译）"}')
    lines.append(f'  拆解粒度：{config.get("granularity", "chapter")}')
    lines.append(f'  数据目录：{bd}')
    lines.append(f'')
    lines.append(f'【卡片转化情况】')
    lines.append(f'  知识点总数：{total}')
    lines.append(f'  含配图：{has_img} 张')
    lines.append(f'  含相关链接：{has_links} 张')
    lines.append(f'  含术语表：{has_terms} 张')
    lines.append(f'  推送周期：每工作日 1 张，约 {total // 5} 周')
    lines.append(f'  已推送：{pushed} / {total}')
    lines.append(f'')
    lines.append(f'【推送方式】')
    lines.append(f'  模板：{config.get("template", "pdf-standard")} → {template_names.get(config.get("template","pdf-standard"), "未知")}')
    push_method = config.get('pushMethod', 'local')
    lines.append(f'  推送通道：{push_method}')
    if push_method == 'local':
        lines.append(f'  本地输出目录：{config.get("local", {}).get("outDir") or "[默认：书籍数据目录]"}')
    if push_method == 'ima':
        lines.append(f'  IMA 知识库：{config.get("ima", {}).get("kbName", "[未设置]")}')
        lines.append(f'  目标文件夹：{config.get("ima", {}).get("folderName", "[未设置]")}')
    elif push_method == 'feishu':
        webhook = config.get('feishu', {}).get('webhook') or '[未设置]'
        lines.append(f'  飞书 Webhook：{webhook[:50]}{"..." if len(webhook) > 50 else ""}')
    elif push_method == 'feishu-api':
        fa = config.get('feishuApi', {}) or {}
        app_id = fa.get('appId') or '[未设置]'
        lines.append(f'  飞书 App ID：{app_id[:20]}{"..." if len(app_id) > 20 else ""}')
        lines.append(f'  飞书 App Secret：{"[已设置]" if fa.get("appSecret") else "[未设置]"}')
        lines.append(f'  飞书 Chat ID：{fa.get("chatId", "[未设置]")}')
    if config.get("imageFormat"):
        lines.append(f'  图片格式：{config.get("imageFormat")}')
    lines.append(f'  测试推送：{"是" if config.get("testPush") else "否"}')
    lines.append(f'')
    lines.append(f'【失败通知】')
    _notify = config.get('notifyWebhook') or '[未设置]'
    lines.append(f'  通知 Webhook：{_notify[:50]}{"..." if len(_notify) > 50 else ""}')
    lines.append(f'')
    lines.append(f'【文件清单】')
    for fn in ['config.json', 'items.json', 'index.json', 'progress.json', 'daily-progress.md']:
        p = os.path.join(bd, fn)
        if os.path.exists(p):
            lines.append(f'  [OK] {fn} ({os.path.getsize(p)} bytes)')
        else:
            lines.append(f'  [MISSING] {fn} (未生成)')
    cards_dir = os.path.join(bd, 'cards')
    if os.path.isdir(cards_dir):
        lines.append(f'  [OK] cards/ ({len(os.listdir(cards_dir))} 张)')
    img_dir = os.path.join(bd, 'images')
    if os.path.isdir(img_dir):
        lines.append(f'  [OK] images/ ({len(os.listdir(img_dir))} 张)')
    lines.append(f'')
    lines.append(f'═══════════════════════════════════════════════════')
    lines.append(f'  请确认以上配置是否正确。如需调整，修改 {bd}/config.json')
    lines.append(f'  确认无误后，运行 prompt 命令获取定时任务提示词：')
    lines.append(f'  python3 book_setup.py prompt {args.slug}')
    lines.append(f'═══════════════════════════════════════════════════')
    print('\n'.join(lines))

def cmd_log_progress(args):
    """Append a record to daily-progress.md after a successful push."""
    bd = book_dir(args.slug)
    dp_path = os.path.join(bd, 'daily-progress.md')
    config = json.load(open(os.path.join(bd, 'config.json'), encoding='utf-8'))
    items = items_io.load_items(bd)  # 兼容两种布局
    card_id = args.card_id
    item = next((it for it in items if isinstance(it, dict) and it.get('id') == card_id), {})
    topic = item.get('topic', '')
    # find card index（精确匹配文件名，子串匹配会在 id 互为前缀时记错序号）
    index = json.load(open(os.path.join(bd, 'index.json'), encoding='utf-8'))
    card_index = '?'
    want_fn = 'card_%s.html' % card_id
    for i, fn in enumerate(index.get('items', [])):
        if fn == want_fn:
            card_index = i + 1
            break
    today = __import__('datetime').date.today().isoformat()
    push_method = config.get('pushMethod', 'local')
    row = f'| {today} | {card_index}/{index.get("totalCards","?")} | {card_id} | {topic} | {push_method} | [OK] 成功 |\n'
    with open(dp_path, 'a', encoding='utf-8') as f:
        f.write(row)
    print(json.dumps({'ok': True, 'logged': card_id, 'date': today, 'file': dp_path}, ensure_ascii=False))

def cmd_prompt(args):
    """Output the cron task prompt for this book."""
    bd = book_dir(args.slug)
    config = json.load(open(os.path.join(bd, 'config.json'), encoding='utf-8'))
    language = config.get('language', 'en')
    push_method = config.get('pushMethod', 'local')
    slug = args.slug

    sd = SKILL_DIR  # dynamic skill directory
    import tempfile
    tmp = tempfile.gettempdir()
    prefix = config.get('cardPrefix', 'BOOK')
    pdf_name = f"{tmp}/{prefix}_$(date +%F)_<nextId>_<topicZh>.pdf" if language == 'en' else f"{tmp}/{prefix}_$(date +%F)_<nextId>_<topic>.pdf"
    # 推送产物落点（local 模式）
    local_out = (config.get('local', {}) or {}).get('outDir') or bd
    # 数据根若被 B2L_DATA_DIR 重定向，提示词必须带上导出语句，
    # 否则 cron 环境里 push_card.py next/mark 会找不到书目录
    b2l_env = ('export B2L_DATA_DIR=%s\n' % os.environ['B2L_DATA_DIR']) if os.environ.get('B2L_DATA_DIR') else ''
    # 步骤号：英文书比中文书多 3 步（联网核对术语 / 翻译 / 写翻译 JSON）
    s = 6 if language == 'en' else 4
    zh_args = ('--zh ' + tmp + '/b2l_zh.json') if language == 'en' else ''
    prompt = f"""执行 book-to-learn skill：推送《{config.get('bookTitle',slug)}》今日知识点卡片。
书目录：{bd}
skill目录：{sd}
语言：{'英文（需翻译）' if language=='en' else '中文（无需翻译）'}
推送方式：{push_method}
{b2l_env}
严格按以下步骤执行：

1. cd {sd} && python3 push_card.py next --book {slug} > {tmp}/b2l_payload.json
   解析输出。若 skip=true（all_done/weekend/already_pushed/push_in_progress），告知并结束。报错时告知用户并结束。
   成功后记下 nextId。生成文件名时中文名需去除文件名非法字符。

2. 从载荷提取 nextId、terminology、coreIdea、explanation、quote、application、relatedLinks（完整原文以 items.json 为准）。"""
    if language == 'en':
        prompt += f"""
3. 【仅英文书】对 terminology 数组每个术语，使用当前环境中可用的联网搜索工具（WebSearch / SearXNG / 其他搜索 skill）查询其在专业领域的权威中文译法，汇总为 terminologyZh。必须联网核对，不可凭记忆。若环境无搜索工具，告知用户需配置搜索能力。
4. 【仅英文书】将 coreIdea/explanation/quote/application 翻译为简体中文：explanation 按换行分段对应；术语首次出现用「中文（英文）」；explanation/application 含 markdown 链接的保留 url 仅译 text；翻译 relatedLinks 标题生成 relatedLinksZh；**同时翻译 topic（知识点标题）为 topicZh**。
5. 写翻译 JSON 到 {tmp}/b2l_zh.json（含 topicZh/coreIdeaZh/explanationZh/quoteZh/applicationZh/terminologyZh/relatedLinksZh/note）。"""
    else:
        prompt += f"""
3. 【中文书】跳过翻译环节，无需写翻译 JSON。"""
    prompt += f"""
{s}. 生成卡片式 PDF（文件名末尾带知识点中文名）：
   cd {sd} && python3 gen_card_pdf.py --payload {tmp}/b2l_payload.json {zh_args} --out "{pdf_name}" --language {language}
   生成后记下实际 PDF 路径（即本行 --out 的值，替换占位符后）为 $PDF_PATH，后续步骤直接使用 $PDF_PATH，不得另行拼文件名。

{s+1}. 校验（推送前必跑，失败不得带病推送）：
   cd {sd} && python3 validate.py --slug {slug} --payload {tmp}/b2l_payload.json {zh_args}
   输出 ok=true 才继续；有 errors 时按提示修正（译文块数 / 术语译名 / 内容源同步）后重跑本步。

{s+2}. 推送：
"""
    if push_method == 'local':
        prompt += f"""   本模式不外发：把产物落到本地输出目录即可。
   cp "$PDF_PATH" "{local_out}/" && ls -l "{local_out}"
   文件存在即视为推送成功。"""
    elif push_method == 'ima':
        prompt += f"""   cd {sd} && python3 upload_ima.py --file "$PDF_PATH" --config {bd}/config.json --book-dir {bd}
   退出码 0=成功继续下一步；2=密钥失效（已发通知）不计进度结束；1=其他错误不更新进度结束。"""
    elif push_method == 'feishu-api':
        prompt += f"""   cd {sd} && python3 send_feishu_api.py --payload {tmp}/b2l_payload.json {zh_args} --config {bd}/config.json --language {language} --file "$PDF_PATH"
   输出 JSON ok=true 则成功（退出码 0）；失败先修复再重试。"""
    else:  # feishu（webhook）
        prompt += f"""   cd {sd} && python3 send_feishu.py --payload {tmp}/b2l_payload.json {zh_args} --config {bd}/config.json --language {language}
   sent=true ok=true 则成功。"""
    dest = {'local': f'本地目录（{local_out}）', 'ima': 'IMA 知识库',
            'feishu': '飞书（webhook）', 'feishu-api': '飞书（Open API）'}.get(push_method, push_method)
    prompt += f"""
{s+3}. 仅成功后记录进度（两步）：
   cd {sd} && python3 push_card.py mark --book {slug} <nextId> success
   cd {sd} && python3 book_setup.py log-progress {slug} --card-id <nextId>
   若任一步失败：cd {sd} && python3 push_card.py mark --book {slug} <nextId> fail

{s+4}. 【仅 IMA】处理 relatedLinks 中的文件附件（可选增强）：
   cd {sd} && python3 process_attachments.py --payload {tmp}/b2l_payload.json --date $(date +%F) --card-id <nextId> --out-dir {tmp}/b2l_attachments
   读取 {tmp}/b2l_attachments/attachments.json，对 processed 数组逐个：python3 upload_ima.py --file <local_path> --config {bd}/config.json --book-dir {bd}
   附件上传失败不影响主进度，但需在汇报中说明。

{s+5}. 汇报：今日推送第 X/N 张、主题、{"术语核对要点、" if language=='en' else ""}附件情况、已推送至{dest}、进度已记录至 daily-progress.md。"""
    print(prompt)

def main():
    ap = argparse.ArgumentParser(description='Book-to-learn setup orchestrator')
    sub = ap.add_subparsers(dest='cmd')
    e = sub.add_parser('extract'); e.add_argument('file'); e.add_argument('--slug', required=True)
    i = sub.add_parser('init'); i.add_argument('slug'); i.add_argument('--title'); i.add_argument('--lang', default='en', choices=['zh','en']); i.add_argument('--granularity', default='chapter'); i.add_argument('--prefix'); i.add_argument('--force', action='store_true')
    # slug 一律位置参数；同时兼容旧文档的 --slug 写法（两种都接受）
    for name in ('gen-cards', 'gen-index', 'download-imgs', 'summary', 'log-progress', 'prompt'):
        p2 = sub.add_parser(name)
        p2.add_argument('slug', nargs='?', default=None)
        p2.add_argument('--slug', dest='slug_opt', default=None, help='与位置参数等价（兼容旧文档写法）')
        if name == 'log-progress':
            p2.add_argument('--card-id', required=True)
    args = ap.parse_args()
    if args.cmd in ('gen-cards', 'gen-index', 'download-imgs', 'summary', 'log-progress', 'prompt'):
        args.slug = args.slug or args.slug_opt
        if not args.slug:
            ap.error('%s 需要一个 slug（位置参数或 --slug）' % args.cmd)
    try:
        {'extract': cmd_extract, 'init': cmd_init, 'gen-cards': cmd_gen_cards,
         'gen-index': cmd_gen_index, 'download-imgs': cmd_download_imgs,
         'summary': cmd_summary, 'log-progress': cmd_log_progress, 'prompt': cmd_prompt
        }.get(args.cmd, lambda a: ap.print_help())(args)
    except SystemExit:
        raise
    except Exception as ex:  # 保持输出 JSON 可解析：缺失/损坏文件不再裸 traceback
        print(json.dumps({'ok': False, 'error': '%s: %s' % (type(ex).__name__, ex)},
                         ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
