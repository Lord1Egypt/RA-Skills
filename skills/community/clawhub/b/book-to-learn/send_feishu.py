#!/usr/bin/env python3
"""
Send a knowledge card as a Feishu interactive card message via webhook.
Alternative to IMA PDF upload.

Usage:
  python send_feishu.py --payload <payload.json> [--zh <zh.json>] --config <config.json> [--language <zh|en>]

Image handling: Feishu cards need image_key or URL. We upload images to a
free image host (catbox.moe, no registration) and embed the URL.
Falls back to appending image URL as text if upload fails.
"""
import json, sys, os, argparse, urllib.request, urllib.parse, base64, re, subprocess
from normalize_quotes import normalize_all

def load_config(path):
    return json.load(open(path, encoding='utf-8'))

def esc_md(text):
    """Escape special chars for Feishu markdown."""
    if not text: return ''
    return text.replace('\\', '\\\\').replace('*', '\\*').replace('_', '\\_').replace('[', '\\[')

def md_links_to_feishu(text):
    """Convert markdown [text](url) to Feishu-compatible link text (url)."""
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: '%s (%s)' % (m.group(1), m.group(2)), text or '')

def upload_to_catbox(image_data, ext='png'):
    """Upload image bytes to catbox.moe (free, no registration). Returns URL or None."""
    try:
        boundary = '----book2learn' + str(hash(image_data) % 10000)
        body = b''
        body += ('--%s\r\n' % boundary).encode()
        body += b'Content-Disposition: form-data; name="reqtype"\r\n\r\n'
        body += b'fileupload\r\n'
        body += ('--%s\r\n' % boundary).encode()
        body += ('Content-Disposition: form-data; name="fileToUpload"; filename="img.%s"\r\n' % ext).encode()
        body += ('Content-Type: image/%s\r\n\r\n' % ext).encode()
        body += image_data
        body += ('\r\n--%s--\r\n' % boundary).encode()
        req = urllib.request.Request('https://catbox.moe/user/api.php', data=body,
                                     headers={'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
                                              'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=60)
        url = resp.read().decode('utf-8').strip()
        if url.startswith('https://') or url.startswith('http://'):
            return url
    except Exception:
        pass
    return None

def decode_data_uri(data_uri):
    """Extract (bytes, ext) from a data:image/...;base64,... URI. Returns (None, None) if not data URI."""
    m = re.match(r'data:image/(\w+);base64,(.+)', data_uri or '', re.S)
    if not m:
        return None, None
    ext = m.group(1)
    if ext == 'jpeg': ext = 'jpg'
    try:
        return base64.b64decode(m.group(2)), ext
    except Exception:
        return None, None

def build_card(payload, zh, language='en'):
    idx = payload.get('cardIndex', '?')
    total = payload.get('totalCards', '?')
    topic = payload.get('topic', '')
    chapter = payload.get('chapter', '')
    book_title = payload.get('bookTitle', '')
    bilingual = language == 'en' and zh

    elements = []

    # progress + chapter
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md",
                 "content": f"**第 {idx} / {total} 张** · {esc_md(chapter)}"}
    })
    elements.append({"tag": "hr"})

    # terminology
    terms_zh = (zh or {}).get('terminologyZh', {})
    terms_en = payload.get('terminology', [])
    if bilingual and terms_zh:
        rows = '\n'.join(f"| {esc_md(en)} | {esc_md(cn)} |" for en, cn in terms_zh.items())
        elements.append({"tag": "markdown",
                         "content": f"**术语对照 · Terminology**\n| EN | 中文 |\n|---|---|\n{rows}"})
        elements.append({"tag": "hr"})
    elif terms_en:
        chips = ' '.join('`%s`' % esc_md(t) for t in terms_en)
        elements.append({"tag": "markdown", "content": f"**关键术语**\n{chips}"})
        elements.append({"tag": "hr"})

    # content sections
    def section(title, zh_text, en_text, md=False):
        parts = []
        if zh_text:
            t = md_links_to_feishu(zh_text) if md else zh_text
            parts.append(f"**{title}**\n{esc_md(t)}")
        if en_text and bilingual:
            t = md_links_to_feishu(en_text) if md else en_text
            parts.append(f"*{t}*")
        if parts:
            elements.append({"tag": "markdown", "content": '\n\n'.join(parts)})
            elements.append({"tag": "hr"})

    if bilingual:
        section("核心观点 · Core Idea", zh.get('coreIdeaZh',''), payload.get('coreIdea',''))
        section("详细解释 · Explanation", zh.get('explanationZh',''), payload.get('explanation',''), md=True)
        section("金句 · Key Quote", zh.get('quoteZh',''), payload.get('quote',''))
        section("应用场景 · Application", zh.get('applicationZh',''), payload.get('application',''), md=True)
    else:
        label = '核心观点' if language == 'zh' else 'Core Idea'
        section(label, payload.get('coreIdea',''), '')
        label2 = '详细解释' if language == 'zh' else 'Explanation'
        section(label2, payload.get('explanation',''), '', md=True)
        label3 = '金句' if language == 'zh' else 'Key Quote'
        section(label3, payload.get('quote',''), '')
        label4 = '应用场景' if language == 'zh' else 'Application'
        section(label4, payload.get('application',''), '', md=True)

    # image
    img = payload.get('image', '')
    if img:
        img_bytes, ext = decode_data_uri(img)
        if img_bytes:
            url = upload_to_catbox(img_bytes, ext)
            if url:
                elements.append({"tag": "img", "url": url, "alt": {"tag": "plain_text", "content": "配图"}})
            else:
                elements.append({"tag": "markdown", "content": "📷 配图（上传失败，见来源链接）"})
        else:
            # image is a URL
            elements.append({"tag": "img", "url": img, "alt": {"tag": "plain_text", "content": "配图"}})
        elements.append({"tag": "hr"})

    # related links
    rl = payload.get('relatedLinks', [])
    rl_zh = (zh or {}).get('relatedLinksZh', []) if bilingual else []
    zh_map = {item['href']: item.get('textZh', '') for item in rl_zh if isinstance(item, dict) and item.get('href')}
    if rl:
        link_lines = []
        for l in rl:
            if isinstance(l, dict):
                href = l.get('href',''); text_en = l.get('text','')
            else:
                href = str(l); text_en = ''
            text_zh = zh_map.get(href, '')
            label = '%s / %s' % (text_zh, text_en) if (text_zh and text_en) else (text_zh or text_en or href)
            link_lines.append(f"• {esc_md(label)}\n  {href}")
        elements.append({"tag": "markdown", "content": "**相关链接 · Related Links**\n" + '\n'.join(link_lines)})
        elements.append({"tag": "hr"})

    # source
    src = payload.get('source', '')
    if src:
        elements.append({"tag": "note", "elements": [{"tag": "plain_text", "content": "来源 / Source: " + src}]})

    card = {
        "header": {
            "title": {"tag": "plain_text", "content": f"📚 {esc_md(book_title)} · {esc_md(topic)}"},
            "template": "blue"
        },
        "elements": elements
    }
    return {"msg_type": "interactive", "card": card}

def send(webhook_url, card_json):
    body = json.dumps(card_json, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(webhook_url, data=body, headers={
        "Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0"})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.load(resp)
        ok = data.get("code") == 0 or data.get("StatusCode") == 0
        print(json.dumps({"sent": True, "ok": ok, "resp": data}, ensure_ascii=False))
        return 0 if ok else 1
    except Exception as e:
        print(json.dumps({"sent": False, "error": str(e)}, ensure_ascii=False))
        return 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--payload', required=True)
    ap.add_argument('--zh', help='translation JSON (English books)')
    ap.add_argument('--config', required=True)
    ap.add_argument('--language', default='en', choices=['zh', 'en'])
    args = ap.parse_args()
    payload = json.load(open(args.payload, encoding='utf-8'))
    zh = json.load(open(args.zh, encoding='utf-8')) if args.zh else None
    config = load_config(args.config)
    webhook = config.get('feishu', {}).get('webhook', '')
    if not webhook:
        print(json.dumps({'ok': False, 'error': 'feishu.webhook not set in config.json'}, ensure_ascii=False))
        sys.exit(1)
    language = args.language or payload.get('language', 'en')
    zh, payload = normalize_all(zh, payload, language)  # 规范化中文引号
    card = build_card(payload, zh, language)
    sys.exit(send(webhook, card))

if __name__ == '__main__':
    main()
