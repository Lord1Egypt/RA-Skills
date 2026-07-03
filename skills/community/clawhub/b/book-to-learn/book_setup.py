#!/usr/bin/env python3
"""
Book setup orchestrator for book-to-learn.
Handles the one-time book decomposition: extract → analyze → outline → generate.

This script provides the extraction + scaffolding infrastructure.
The actual AI analysis (chapter detection, knowledge point generation) is
performed by the AI agent following SKILL.md instructions, using these helpers:

  python book_setup.py extract <file> --slug <slug>          Extract text → books/<slug>/full_text.txt
  python book_setup.py init <slug> --title "..." --lang <zh|en>  Create config.json skeleton
  python book_setup.py gen-cards --slug <slug>               Generate cards/ from items.json
  python book_setup.py gen-index --slug <slug>               Generate index.json from items.json
  python book_setup.py download-imgs --slug <slug>           Download images, embed as base64
  python book_setup.py prompt --slug <slug>                  Output the cron prompt for this book
"""
import json, os, sys, re, base64, hashlib, subprocess, argparse, urllib.request

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(SKILL_DIR, 'books')

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
        'bookTitle': args.title or args.slug,
        'bookSlug': args.slug,
        'language': args.lang,
        'pushMethod': 'ima',
        'ima': {'kbName': '', 'folderName': ''},
        'feishu': {'webhook': ''},
        'notifyWebhook': '',
        'granularity': args.granularity,
        'cardPrefix': args.prefix or 'BOOK',
        'template': 'pdf-standard',  # pdf-standard | pdf-large | feishu-card | feishu-card+image
        'imageFormat': '1:1',  # 1:1 | 1:4 (only for image supplement)
        'testPush': False,  # whether to do a test push after setup
        'createdAt': __import__('datetime').date.today().isoformat(),
    }
    with open(cfg_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(json.dumps({'ok': True, 'config': cfg_path, 'config_content': config}, ensure_ascii=False, indent=2))

def cmd_gen_cards(args):
    """Generate cards/*.html from items.json (English source cards with translation-panel)."""
    bd = book_dir(args.slug)
    items = json.load(open(os.path.join(bd, 'items.json'), encoding='utf-8'))
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
    items = json.load(open(os.path.join(bd, 'items.json'), encoding='utf-8'))
    config = json.load(open(os.path.join(bd, 'config.json'), encoding='utf-8'))
    index = {
        'bookTitle': config.get('bookTitle', args.slug),
        'bookSource': items[0].get('link', '') if items else '',
        'totalCards': len(items),
        'items': ['card_%s.html' % it['id'] for it in items]
    }
    with open(os.path.join(bd, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    # also init progress.json if not exists
    prog_path = os.path.join(bd, 'progress.json')
    if not os.path.exists(prog_path):
        with open(prog_path, 'w', encoding='utf-8') as f:
            json.dump({'lastPushedId': None, 'lastPushDate': None, 'pushHistory': []}, f, ensure_ascii=False, indent=2)
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
    items = json.load(open(os.path.join(bd, 'items.json'), encoding='utf-8'))
    img_dir = os.path.join(bd, 'images')
    os.makedirs(img_dir, exist_ok=True)
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
    url_map = {}
    for it in items:
        u = it.get('image', '')
        if u and not u.startswith('data:') and u not in url_map:
            ext = u.rsplit('.', 1)[-1].split('?')[0].split('-')[0].lower()
            if ext not in ('png','jpg','jpeg','gif','webp','svg'): ext = 'png'
            if ext == 'jpeg': ext = 'jpg'
            h = hashlib.md5(u.encode()).hexdigest()[:10]
            fn = f'img_{h}.{ext}'
            out = os.path.join(img_dir, fn)
            for attempt in range(3):
                r = subprocess.run(['curl','-sL','--insecure','--max-time','30','-A',UA,'-o',out,u], capture_output=True)
                if os.path.exists(out) and os.path.getsize(out) > 500:
                    head = open(out,'rb').read(8)
                    if head[:4]==b'\x89PNG' or head[:3]==b'\xff\xd8\xff' or head[:4]==b'GIF8' or head[:4]==b'RIFF':
                        url_map[u] = fn
                        break
                if os.path.exists(out) and os.path.getsize(out) <= 500:
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
    # update items.json
    updated = 0
    for it in items:
        u = it.get('image','')
        if u in data_uris:
            it['image'] = data_uris[u]
            updated += 1
    with open(os.path.join(bd, 'items.json'), 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(json.dumps({'ok': True, 'downloaded': len(url_map), 'embedded': updated, 'slug': args.slug}, ensure_ascii=False))

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
    has_img = sum(1 for it in items if it.get('image', '').startswith('data:'))
    has_links = sum(1 for it in items if it.get('relatedLinks'))
    has_terms = sum(1 for it in items if it.get('terminology'))

    lines = []
    lines.append(f'═══════════════════════════════════════════════════')
    lines.append(f'  📖 《{config.get("bookTitle", args.slug)}》 配置确认')
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
    lines.append(f'  推送通道：{config.get("pushMethod", "ima")}')
    if config.get('pushMethod') == 'ima':
        lines.append(f'  IMA 知识库：{config.get("ima", {}).get("kbName", "⚠️ 未设置")}')
        lines.append(f'  目标文件夹：{config.get("ima", {}).get("folderName", "⚠️ 未设置")}')
    else:
        lines.append(f'  飞书 Webhook：{config.get("feishu", {}).get("webhook", "⚠️ 未设置")[:50]}...')
    if config.get("imageFormat"):
        lines.append(f'  图片格式：{config.get("imageFormat")}')
    lines.append(f'  测试推送：{"是" if config.get("testPush") else "否"}')
    lines.append(f'')
    lines.append(f'【失败通知】')
    lines.append(f'  通知 Webhook：{config.get("notifyWebhook", "⚠️ 未设置")[:50]}{"..." if len(config.get("notifyWebhook",""))>50 else ""}')
    lines.append(f'')
    lines.append(f'【文件清单】')
    for fn in ['config.json', 'items.json', 'index.json', 'progress.json', 'daily-progress.md']:
        p = os.path.join(bd, fn)
        if os.path.exists(p):
            lines.append(f'  ✅ {fn} ({os.path.getsize(p)} bytes)')
        else:
            lines.append(f'  ❌ {fn} (未生成)')
    cards_dir = os.path.join(bd, 'cards')
    if os.path.isdir(cards_dir):
        lines.append(f'  ✅ cards/ ({len(os.listdir(cards_dir))} 张)')
    img_dir = os.path.join(bd, 'images')
    if os.path.isdir(img_dir):
        lines.append(f'  ✅ images/ ({len(os.listdir(img_dir))} 张)')
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
    items = json.load(open(os.path.join(bd, 'items.json'), encoding='utf-8'))
    card_id = args.card_id
    item = next((it for it in items if it['id'] == card_id), {})
    topic = item.get('topic', '')
    # find card index
    index = json.load(open(os.path.join(bd, 'index.json'), encoding='utf-8'))
    card_index = '?'
    for i, fn in enumerate(index.get('items', [])):
        if card_id in fn:
            card_index = i + 1
            break
    today = __import__('datetime').date.today().isoformat()
    push_method = config.get('pushMethod', 'ima')
    row = f'| {today} | {card_index}/{index.get("totalCards","?")} | {card_id} | {topic} | {push_method} | ✅ 成功 |\n'
    with open(dp_path, 'a', encoding='utf-8') as f:
        f.write(row)
    print(json.dumps({'ok': True, 'logged': card_id, 'date': today, 'file': dp_path}, ensure_ascii=False))

def cmd_prompt(args):
    """Output the cron task prompt for this book."""
    bd = book_dir(args.slug)
    config = json.load(open(os.path.join(bd, 'config.json'), encoding='utf-8'))
    language = config.get('language', 'en')
    push_method = config.get('pushMethod', 'ima')
    slug = args.slug

    sd = SKILL_DIR  # dynamic skill directory
    import tempfile
    tmp = tempfile.gettempdir()
    prompt = f"""执行 book-to-learn skill：推送《{config.get('bookTitle',slug)}》今日知识点卡片。
书目录：{bd}
skill目录：{sd}
语言：{'英文（需翻译）' if language=='en' else '中文（无需翻译）'}
推送方式：{push_method}

严格按以下步骤执行：

1. cd {sd} && python3 push_card.py next --book {slug} --force > {tmp}/b2l_payload.json
   解析输出。若 skip=true（all_done/weekend/already_pushed），告知并结束。

2. 从载荷提取 nextId、terminology、coreIdea、explanation、quote、application、relatedLinks。"""
    if language == 'en':
        prompt += f"""
3. 【仅英文书】对 terminology 数组每个术语，使用当前环境中可用的联网搜索工具（WebSearch / SearXNG / 其他搜索 skill）查询其在专业领域的权威中文译法，汇总为 terminologyZh。必须联网核对，不可凭记忆。若环境无搜索工具，告知用户需配置搜索能力。
4. 【仅英文书】将 coreIdea/explanation/quote/application 翻译为简体中文：explanation 按换行分段对应；术语首次出现用「中文（英文）」；explanation/application 含 markdown 链接的保留 url 仅译 text；翻译 relatedLinks 标题生成 relatedLinksZh；**同时翻译 topic（知识点标题）为 topicZh**。
5. 写翻译 JSON 到 {tmp}/b2l_zh.json（含 topicZh/coreIdeaZh/explanationZh/quoteZh/applicationZh/terminologyZh/relatedLinksZh/note）。"""
    else:
        prompt += f"""
3. 【中文书】跳过翻译环节，无需写翻译 JSON。"""
    prompt += f"""
{6 if language=='en' else 4}. 生成卡片式 PDF（文件名末尾带知识点中文名）：
   cd {sd} && python3 gen_card_pdf.py --payload {tmp}/b2l_payload.json {"--zh "+tmp+"/b2l_zh.json" if language=='en' else ""} --out "{tmp}/{config.get('cardPrefix','BOOK')}_$(date +%F)_<nextId>_<{('topicZh' if language=='en' else 'topic')}>.pdf" --language {language}

{7 if language=='en' else 5}. 推送：
"""
    if push_method == 'ima':
        prompt += f"""   cd {sd} && python3 upload_ima.py --file "{tmp}/{config.get('cardPrefix','BOOK')}_<date>_<nextId>.pdf" --config {bd}/config.json --book-dir {bd}
   退出码 0=成功继续下一步；2=密钥失效（已发通知）不计进度结束；1=其他错误不更新进度结束。"""
    else:
        prompt += f"""   cd {sd} && python3 send_feishu.py --payload {tmp}/b2l_payload.json {"--zh "+tmp+"/b2l_zh.json" if language=='en' else ""} --config {bd}/config.json --language {language}
   sent=true ok=true 则成功。"""
    prompt += f"""
{8 if language=='en' else 6}. 仅成功后记录进度（两步）：
   cd {sd} && python3 push_card.py mark --book {slug} <nextId> success
   cd {sd} && python3 book_setup.py log-progress {slug} --card-id <nextId>

{9 if language=='en' else 7}. 汇报：今日推送第 X/N 张、主题、{"术语核对要点、" if language=='en' else ""}已推送至{"IMA知识库" if push_method=='ima' else "飞书"}、进度已记录至 daily-progress.md。"""
    print(prompt)

def main():
    ap = argparse.ArgumentParser(description='Book-to-learn setup orchestrator')
    sub = ap.add_subparsers(dest='cmd')
    e = sub.add_parser('extract'); e.add_argument('file'); e.add_argument('--slug', required=True)
    i = sub.add_parser('init'); i.add_argument('slug'); i.add_argument('--title'); i.add_argument('--lang', default='en', choices=['zh','en']); i.add_argument('--granularity', default='chapter'); i.add_argument('--prefix'); i.add_argument('--force', action='store_true')
    gc = sub.add_parser('gen-cards'); gc.add_argument('slug')
    gi = sub.add_parser('gen-index'); gi.add_argument('slug')
    di = sub.add_parser('download-imgs'); di.add_argument('slug')
    sm = sub.add_parser('summary'); sm.add_argument('slug')
    lp = sub.add_parser('log-progress'); lp.add_argument('slug'); lp.add_argument('--card-id', required=True)
    pr = sub.add_parser('prompt'); pr.add_argument('slug')
    args = ap.parse_args()
    {'extract': cmd_extract, 'init': cmd_init, 'gen-cards': cmd_gen_cards,
     'gen-index': cmd_gen_index, 'download-imgs': cmd_download_imgs,
     'summary': cmd_summary, 'log-progress': cmd_log_progress, 'prompt': cmd_prompt
    }.get(args.cmd, lambda a: ap.print_help())(args)

if __name__ == '__main__':
    main()
