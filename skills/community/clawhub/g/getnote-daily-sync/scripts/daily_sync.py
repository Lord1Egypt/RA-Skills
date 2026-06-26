#!/usr/bin/env python3
"""
getnote-notion-daily — 每日 Get笔记 → Notion 日报同步脚本

环境变量：
  GETNOTE_API_KEY       Get笔记 API Key
  GETNOTE_CLIENT_ID     Get笔记 Client ID
  NOTION_TOKEN          Notion Integration Token
  NOTION_DATABASE_ID    目标 Notion Database ID
  MY_NAME               （可选）用于过滤"我需要跟进"的待办关键词，多个用逗号分隔
                        例如: "Alice,我" 默认留空则显示所有待办
"""
import urllib.request, json, os, re, sys
from datetime import datetime, timezone, timedelta

API_KEY    = os.environ.get('GETNOTE_API_KEY', '')
CLIENT_ID  = os.environ.get('GETNOTE_CLIENT_ID', '')
NOTION_TOKEN = os.environ.get('NOTION_TOKEN', '')
NOTION_DB  = os.environ.get('NOTION_DATABASE_ID', '')
MY_NAME_RAW = os.environ.get('MY_NAME', '')

# 校验必填项
missing = [k for k, v in {
    'GETNOTE_API_KEY': API_KEY,
    'GETNOTE_CLIENT_ID': CLIENT_ID,
    'NOTION_TOKEN': NOTION_TOKEN,
    'NOTION_DATABASE_ID': NOTION_DB,
}.items() if not v]
if missing:
    print(f"❌ 缺少必填环境变量: {', '.join(missing)}", file=sys.stderr)
    sys.exit(1)

# MY_NAME 过滤关键词
my_name_keywords = [n.strip() for n in MY_NAME_RAW.split(',') if n.strip()] if MY_NAME_RAW else []

BASE_URL = 'https://openapi.biji.com/open/api/v1/resource'

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
today = now.strftime('%Y-%m-%d')
weekday_map = {0:'周一',1:'周二',2:'周三',3:'周四',4:'周五',5:'周六',6:'周日'}
weekday = weekday_map[now.weekday()]

def getnote_get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}",
        headers={'Authorization': API_KEY, 'X-Client-ID': CLIENT_ID})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def notion_req(method, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        f"https://api.notion.com/v1{path}",
        data=data, method=method,
        headers={
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())

def append_blocks(page_id, blocks):
    for i in range(0, len(blocks), 50):
        batch = blocks[i:i+50]
        notion_req('PATCH', f'/blocks/{page_id}/children', {"children": batch})

# ── Notion block 构造函数 ──
def b_h2(text):
    return {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"type":"text","text":{"content":text}}]}}

def b_h3(text):
    return {"object":"block","type":"heading_3","heading_3":{"rich_text":[{"type":"text","text":{"content":text}}]}}

def b_para(rich_text_parts):
    return {"object":"block","type":"paragraph","paragraph":{"rich_text": rich_text_parts}}

def b_bullet(rich_text_parts):
    return {"object":"block","type":"bulleted_list_item","bulleted_list_item":{"rich_text": rich_text_parts}}

def b_divider():
    return {"object":"block","type":"divider","divider":{}}

def plain(text):
    return [{"type":"text","text":{"content":text}}]

def parse_inline(text):
    parts = []
    pattern = re.compile(r'\*\*(.+?)\*\*')
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            parts.append({"type":"text","text":{"content":text[last:m.start()]}})
        parts.append({"type":"text","text":{"content":m.group(1)},"annotations":{"bold":True}})
        last = m.end()
    if last < len(text):
        parts.append({"type":"text","text":{"content":text[last:]}})
    return parts if parts else [{"type":"text","text":{"content":text}}]

def md_to_blocks(md_text):
    blocks = []
    for line in md_text.split('\n'):
        line = line.rstrip()
        if not line:
            continue
        if line.startswith('#### ') or line.startswith('### '):
            blocks.append(b_h3(re.sub(r'^#{3,4}\s+', '', line)))
        elif line.startswith('## '):
            blocks.append(b_h2(line[3:].strip()))
        elif re.match(r'^\s*[-*]\s+', line):
            content = re.sub(r'^\s*[-*]\s+', '', line)
            blocks.append(b_bullet(parse_inline(content)))
        else:
            blocks.append(b_para(parse_inline(line)))
    return blocks

def extract_section(content, *keywords):
    lines = content.split('\n')
    result, in_section, section_level = [], False, 0
    for line in lines:
        m = re.match(r'^(#{2,4})\s+', line)
        if m:
            level = len(m.group(1))
            if any(kw in line for kw in keywords):
                in_section, section_level = True, level
                continue
            elif in_section and level <= section_level:
                break
        if in_section:
            result.append(line)
    return '\n'.join(result).strip()

# ── 拉取今天的笔记 ──
notes_today = []
since_id = 0
done = False
while not done:
    data = getnote_get(f'/note/list?since_id={since_id}')
    notes = data.get('data', {}).get('notes', [])
    if not notes:
        break
    for n in notes:
        created = n.get('created_at', '')[:10]
        if created == today:
            notes_today.append(n)
        elif created < today:
            done = True
            break
    since_id = data.get('data', {}).get('next_cursor', 0)
    if not data.get('data', {}).get('has_more'):
        break

if not notes_today:
    print("今日无 Get笔记 记录，跳过总结")
    sys.exit(0)

# ── 分类 ──
AUDIO_TYPES = ('recorder_audio','meeting','local_audio','audio',
               'recorder_flash_audio','class_audio','internal_record')
time_keywords = ['下周','明天','本周','今天','周一','周二','周三','周四',
                 '周五','周六','周日','月','日','号','下下周']
client_meetings, tech_shares, personal = [], [], []

for n in notes_today:
    title   = n.get('title', '(无标题)')
    ntype   = n.get('note_type', '')
    content = n.get('content', '')
    time_str = n.get('created_at', '')[11:16]

    info_md    = extract_section(content, '录音信息')
    summary_md = extract_section(content, '录音总结')
    todo_md    = extract_section(content, '待办事项', '📋 待办事项')

    todos_raw = re.findall(r'[-•]\s*(.+)', todo_md) if todo_md else []
    timed_todos = [(title[:20], t.strip()) for t in todos_raw
                   if any(k in t for k in time_keywords)]

    quotes_md  = extract_section(content, '金句精选')
    first_quote = ''
    if quotes_md:
        q_matches = re.findall(r'[-*]\s*"(.+?)"', quotes_md)
        first_quote = q_matches[0] if q_matches else ''

    first_sentence = ''
    if summary_md:
        first_line = summary_md.strip().split('\n')[0]
        m = re.match(r'^([^。\.]{10,80}[。\.])', first_line)
        first_sentence = m.group(1) if m else first_line[:100]

    entry = {
        'title': title, 'type': ntype, 'time': time_str,
        'info_md': info_md, 'summary_md': summary_md, 'todo_md': todo_md,
        'timed_todos': timed_todos, 'first_sentence': first_sentence,
        'first_quote': first_quote
    }

    is_test    = '测试' in title or (ntype == 'plain_text' and len(content) < 50)
    is_audio   = ntype in AUDIO_TYPES
    is_meeting = is_audio and any(kw in title for kw in ['会议','讨论','对接','-',' - ','沟通','交流','分享'])

    if not is_test:
        if is_meeting: client_meetings.append(entry)
        elif is_audio: tech_shares.append(entry)
        else: personal.append(entry)

# ── Summary 字段 ──
parts = []
if client_meetings: parts.append(f"{len(client_meetings)}客户会")
if tech_shares:     parts.append(f"{len(tech_shares)}技术分享")
if personal:        parts.append(f"{len(personal)}个人灵感")
all_todos_count = sum(len(re.findall(r'[-•]\s*.+', e.get('todo_md','') or ''))
                      for e in client_meetings + tech_shares + personal)
summary_field = ' · '.join(parts) + (f" | 待办{all_todos_count}项" if all_todos_count else " | 无待办")

# ── 创建 Notion 页面 ──
page_title = f"日报 · {today}（{weekday}）"
page = notion_req('POST', '/pages', {
    "parent": {"database_id": NOTION_DB},
    "properties": {
        "Name": {"title": [{"text": {"content": page_title}}]},
        "date": {"date": {"start": today}},
        "Summary": {"rich_text": [{"text": {"content": summary_field}}]},
        "Tags": {"multi_select": [{"name": "日报"}]},
        "Source": {"select": {"name": "Get笔记"}}
    }
})
page_id  = page['id']
page_url = page['url']

# ── 写正文 ──
blocks = []
blocks.append(b_h2(f"📋 今日笔记总结 · {today}（{weekday}）"))
blocks.append(b_para(plain(f"共 {len(notes_today)} 条笔记 | {summary_field}")))
blocks.append(b_divider())

# 今日概览
blocks.append(b_h2("📊 今日概览"))
blocks.append(b_h3("今天做了什么"))
for e in client_meetings + tech_shares + personal:
    if e['first_sentence']:
        blocks.append(b_bullet(parse_inline(f"**{e['title'][:25]}**：{e['first_sentence']}")))

# 待办过滤：有 MY_NAME 则过滤，无则全部显示
all_todos_flat = []
for e in client_meetings + tech_shares + personal:
    for t in re.findall(r'[-•]\s*(.+)', e.get('todo_md','') or ''):
        all_todos_flat.append((e['title'][:15], t.strip()))

blocks.append(b_h3("🔥 最需要跟进的事情"))
if my_name_keywords:
    timed   = [(s,t) for s,t in all_todos_flat if any(k in t for k in time_keywords) and any(k in t for k in my_name_keywords)]
    others  = [(s,t) for s,t in all_todos_flat if not any(k in t for k in time_keywords) and any(k in t for k in my_name_keywords)]
    top3    = (timed + others)[:3]
else:
    timed   = [(s,t) for s,t in all_todos_flat if any(k in t for k in time_keywords)]
    top3    = (timed + [x for x in all_todos_flat if x not in timed])[:3]

if top3:
    for src, t in top3:
        blocks.append(b_bullet(plain(f"【{src}】{t}")))
else:
    blocks.append(b_para(plain("今日暂无待办")))

quotes = [(e['title'][:15], e['first_quote']) for e in client_meetings + tech_shares + personal if e.get('first_quote')]
if quotes:
    blocks.append(b_h3("💡 今日关键洞察"))
    for src, q in quotes:
        blocks.append(b_bullet(parse_inline(f'**【{src}】** \u201c{q}\u201d')))
blocks.append(b_divider())

def add_note(entry, emoji, label):
    blocks.append(b_h2(f"{emoji} {label} · {entry['title']} ({entry['time']})"))
    if entry['info_md']:
        blocks.append(b_h3("录音信息"))
        blocks.extend(md_to_blocks(entry['info_md']))
    if entry['summary_md']:
        blocks.append(b_h3("录音总结"))
        blocks.extend(md_to_blocks(entry['summary_md']))
    if entry['todo_md']:
        blocks.append(b_h3("待办事项"))
        blocks.extend(md_to_blocks(entry['todo_md']))
    blocks.append(b_divider())

for e in client_meetings: add_note(e, '🗣️', '客户会')
for e in tech_shares:     add_note(e, '🎤', '技术分享')
for e in personal:        add_note(e, '💡', '个人')

# 后续建议
all_timed = []
for e in client_meetings + tech_shares + personal:
    all_timed.extend(e['timed_todos'])

blocks.append(b_h2("📌 后续建议"))
if all_timed:
    for src, t in all_timed:
        blocks.append(b_bullet(plain(f"【{src}】{t}")))
else:
    blocks.append(b_para(plain("各项待办暂无明确时间安排")))

append_blocks(page_id, blocks)
print(f"✅ 今日笔记总结已存入 Notion，共 {len(notes_today)} 条笔记")
print(f"🔗 {page_url}")
