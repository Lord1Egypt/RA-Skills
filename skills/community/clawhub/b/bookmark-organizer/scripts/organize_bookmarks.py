#!/usr/bin/env python3
from html.parser import HTMLParser
from urllib.parse import urlparse, urlunparse
from collections import defaultdict, Counter
from pathlib import Path
import re
import sys

class BookmarkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_folder = ''
        self.in_h3 = False
        self.h3_text = ''
        self.in_a = False
        self.a_href = ''
        self.a_text = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h3':
            self.in_h3 = True
            self.h3_text = ''
        elif tag == 'a':
            self.in_a = True
            self.a_href = attrs.get('href', '')
            self.a_text = ''

    def handle_endtag(self, tag):
        if tag == 'h3' and self.in_h3:
            self.current_folder = self.h3_text.strip()
            self.in_h3 = False
        elif tag == 'a' and self.in_a:
            self.links.append({
                'title': self.a_text.strip(),
                'url': self.a_href,
                'folder': self.current_folder,
            })
            self.in_a = False

    def handle_data(self, data):
        if self.in_h3:
            self.h3_text += data
        if self.in_a:
            self.a_text += data


def normalize_url(url: str) -> str:
    try:
        u = urlparse(url)
        return urlunparse((u.scheme, u.netloc.lower(), u.path.rstrip('/'), '', '', ''))
    except Exception:
        return url


def classify(item):
    text = f"{item['title']} {item['url']} {item['folder']}".lower()
    rules = [
        ('adult-or-sensitive', [r'porn', r'jav', r'laowang', r'51cg', r'yanshe']),
        ('ai-dev', [r'openai', r'clawhub', r'huggingface', r'github', r'colab', r'civitai', r'fal\.ai', r'cursor', r'vscode', r'python', r'api', r'docs', r'model', r'ai']),
        ('games-mods', [r'nexusmods', r'3dmgame', r'xianyudanji', r'game', r'mod', r'steam', r'rom', r'emu']),
        ('learning', [r'wikipedia', r'zhihu', r'blogspot', r'publicdomainreview', r'arxiv', r'tutorial', r'guide', r'course']),
        ('design-art', [r'artstation', r'behance', r'dribble', r'pixiv', r'image', r'design', r'inspiration', r'gallery']),
        ('video-media', [r'youtube', r'bilibili', r'vimeo', r'netflix', r'meijutt', r'movie', r'video']),
    ]
    for name, pats in rules:
        if any(re.search(p, text) for p in pats):
            return name
    if 'group ' in text or 'tabs set aside' in text or '已搁置' in text or '组 ' in text:
        return 'tab-groups'
    return 'misc'


def write_list(path: Path, title: str, items):
    with path.open('w', encoding='utf-8') as f:
        f.write(f'# {title}\n\n共 {len(items)} 条\n\n')
        for item in items:
            folder = item.get('folder', '')
            extra = f'  · 文件夹: {folder}' if folder else ''
            f.write(f"- [{item['title'] or item['url']}]({item['url']}){extra}\n")


def main():
    if len(sys.argv) != 3:
        print('Usage: organize_bookmarks.py <bookmarks.html> <output_dir>')
        sys.exit(2)

    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)

    html = src.read_text(encoding='utf-8', errors='ignore')
    parser = BookmarkParser()
    parser.feed(html)
    links = parser.links

    buckets = defaultdict(list)
    for item in links:
        buckets[classify(item)].append(item)

    write_list(out / 'ai-dev.md', 'ai-dev', buckets['ai-dev'])
    write_list(out / 'games-mods.md', 'games-mods', buckets['games-mods'])
    write_list(out / 'learning.md', 'learning', buckets['learning'])
    write_list(out / 'design-art.md', 'design-art', buckets['design-art'])
    write_list(out / 'video-media.md', 'video-media', buckets['video-media'])
    write_list(out / 'tab-groups.md', 'tab-groups', buckets['tab-groups'])
    write_list(out / 'adult-or-sensitive.md', 'adult-or-sensitive', buckets['adult-or-sensitive'])
    write_list(out / 'misc.md', 'misc', buckets['misc'])

    domains = Counter(urlparse(x['url']).netloc.lower() for x in links if x['url'].startswith('http'))
    folders = [x['folder'] for x in links if x['folder']]
    with (out / '_index.md').open('w', encoding='utf-8') as f:
        f.write('# 书签库索引\n\n')
        f.write(f'- 总链接数：{len(links)}\n')
        f.write(f'- 文件夹数：{len(set(folders))}\n\n')
        f.write('## 高频域名\n')
        for domain, n in domains.most_common(25):
            f.write(f'- {n} · {domain}\n')

    by_url = defaultdict(list)
    for item in links:
        if item['url'].startswith('http'):
            by_url[normalize_url(item['url'])].append(item)
    dups = [v for v in by_url.values() if len(v) > 1]
    with (out / 'duplicates.md').open('w', encoding='utf-8') as f:
        f.write(f'# 重复书签\n\n重复URL组数：{len(dups)}\n\n')
        for grp in sorted(dups, key=len, reverse=True)[:120]:
            f.write(f"## {grp[0]['url']} · 重复 {len(grp)} 次\n")
            for item in grp:
                f.write(f"- {item['title'] or item['url']} · 文件夹: {item['folder']}\n")
            f.write('\n')

    ai_rows = []
    seen = set()
    for item in buckets['ai-dev']:
        if item['url'] in seen:
            continue
        seen.add(item['url'])
        domain = urlparse(item['url']).netloc.lower() if item['url'].startswith('http') else ''
        kind = 'AI/开发'
        text = f"{item['title']} {item['url']}".lower()
        if 'clawhub' in text:
            kind = 'OpenClaw/技能'
        elif 'huggingface' in text:
            kind = '模型/开源AI'
        elif 'civitai' in text:
            kind = 'AI绘图/模型'
        elif 'colab' in text:
            kind = '云端开发/Notebook'
        elif 'github' in text:
            kind = '代码/开发'
        ai_rows.append((item['title'] or domain, domain, kind, item['folder'], item['url']))

    with (out / 'ai-tools-table.md').open('w', encoding='utf-8') as f:
        f.write('# AI 工具相关网站总表\n\n')
        f.write('| 名称 | 域名 | 类型 | 所在文件夹 | 链接 |\n')
        f.write('|---|---|---|---|---|\n')
        for title, domain, kind, folder, url in ai_rows:
            title = title.replace('|', ' ')
            folder = (folder or '').replace('|', ' ')
            f.write(f'| {title} | {domain} | {kind} | {folder} | {url} |\n')

    with (out / 'query-index.md').open('w', encoding='utf-8') as f:
        f.write('# 书签功能索引\n\n')
        f.write('- AI / 开发 → `ai-dev.md` / `ai-tools-table.md`\n')
        f.write('- 游戏 / Mod → `games-mods.md`\n')
        f.write('- 学习 / 资料 → `learning.md`\n')
        f.write('- 设计 / 灵感 → `design-art.md`\n')
        f.write('- 视频 / 媒体 → `video-media.md`\n')
        f.write('- 临时标签页 → `tab-groups.md`\n')
        f.write('- 重复项 → `duplicates.md`\n')

    with (out / 'recommended-shortlist.md').open('w', encoding='utf-8') as f:
        f.write('# 常用网站推荐清单（基于你的书签）\n\n')
        picks = {
            'AI与开发': ['clawhub.ai', 'huggingface.co', 'colab.research.google.com', 'civitai.com'],
            '游戏与Mod': ['www.nexusmods.com', 'dl.3dmgame.com', 'www.xianyudanji.to'],
            '资料与阅读': ['publicdomainreview.org', 'en.wikipedia.org', 'zhuanlan.zhihu.com'],
            '设计与灵感': ['www.artstation.com'],
            '视频与媒体': ['www.youtube.com', 'www.meijutt.com'],
        }
        for cat, ds in picks.items():
            f.write(f'## {cat}\n')
            for d in ds:
                if domains[d]:
                    f.write(f'- {d}（收藏 {domains[d]} 次）\n')
            f.write('\n')

if __name__ == '__main__':
    main()
