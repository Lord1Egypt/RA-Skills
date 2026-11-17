#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_site.py — 在线文档站抓取（网站模式的「拆书」阶段）

把文档站（Mintlify / Docusaurus / VitePress 等）抓成一套可继续处理的数据：

    books/<slug>/raw/pages/*.md     每页正文（优先抓 `<url>.md` 源，比抓 HTML 干净）
    books/<slug>/raw/imgs/*          正文配图（下划线扁平化命名，便于映射）
    books/<slug>/catalog.json        全量清单（idx / 章节 / 标题 / 链接 / 父页）

两条通道互相印证，避免漏页：
    通道 A：sitemap.xml（全量，权威）
    通道 B：首页导航链接（补 sitemap 缺失的新页面）

用法：
    python fetch_site.py --base-url https://docs.example.com --slug mydocs
        [--sitemap auto|<url>] [--include /start] [--exclude /start/hubs /]...
        [--body-suffix .md] [--limit 300] [--no-images] [--urls-file urls.txt]
        [--delay 0.1] [--timeout 20]

输出 JSON：{ok, slug, urls, pages, images, catalog}
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.environ.get('B2L_DATA_DIR') or os.path.join(SKILL_DIR, 'books')
UA = 'book-to-learn/1.5 (+site-fetch)'

LOC_RE = re.compile(r'<loc>\s*([^<\s]+)\s*</loc>', re.I)
HREF_RE = re.compile(r'<a\s[^>]*href\s*=\s*"([^"]+)"', re.I)
IMG_RE = re.compile(r'<img\s[^>]*?src\s*=\s*"([^"]+)"[^>]*?/?>', re.I)
TITLE_RE = re.compile(r'^#\s+(.+)$', re.M)


def http_get(url, timeout=20, binary=False):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data if binary else data.decode('utf-8', 'replace')


def norm_url(u, base):
    """相对 → 绝对；去掉 query / fragment / 尾斜杠。"""
    u = urllib.parse.urljoin(base, u)
    p = urllib.parse.urlsplit(u)
    path = p.path.rstrip('/') or '/'
    return urllib.parse.urlunsplit((p.scheme, p.netloc, path, '', ''))


def fetch_sitemap(base_url, sitemap, timeout):
    """通道 A：sitemap.xml"""
    candidates = []
    if sitemap and sitemap != 'auto':
        candidates.append(sitemap)
    else:
        candidates += [urllib.parse.urljoin(base_url, '/sitemap.xml'),
                       urllib.parse.urljoin(base_url, '/sitemap-0.xml')]
    for c in candidates:
        try:
            xml = http_get(c, timeout=timeout)
            # 先判 sitemap 索引再取 <loc>：索引里的 <loc> 是子 sitemap 地址而不是页面，
            # 必须抓子 sitemap 展开（支持一层嵌套索引）
            if '<sitemapindex' in xml.lower():
                urls = []
                for sub in LOC_RE.findall(xml)[:25]:
                    try:
                        sub_xml = http_get(sub, timeout=timeout)
                        if '<sitemapindex' in sub_xml.lower():
                            for sub2 in LOC_RE.findall(sub_xml)[:25]:
                                try:
                                    leaf = http_get(sub2, timeout=timeout)
                                    if '<sitemapindex' not in leaf.lower():
                                        urls += [norm_url(u, base_url) for u in LOC_RE.findall(leaf)]
                                except Exception:
                                    continue
                        else:
                            urls += [norm_url(u, base_url) for u in LOC_RE.findall(sub_xml)]
                    except Exception:
                        continue
                if urls:
                    return urls, c
                continue
            urls = [norm_url(u, base_url) for u in LOC_RE.findall(xml)]
            if urls:
                return urls, c
        except Exception:
            continue
    return [], None


def fetch_nav(base_url, timeout):
    """通道 B：首页导航链接（补 sitemap 缺失的新页面）。"""
    try:
        html = http_get(base_url, timeout=timeout)
    except Exception:
        return []
    origin = '{u.scheme}://{u.netloc}'.format(u=urllib.parse.urlsplit(base_url))
    out = []
    for href in HREF_RE.findall(html):
        if href.startswith(('#', 'mailto:', 'javascript:')):
            continue
        u = norm_url(href, base_url)
        if u.startswith(origin) and not re.search(r'\.(png|jpe?g|svg|css|js|xml|txt|ico|webp|gif)$', u, re.I):
            out.append(u)
    return out


def keep(url, base_url, include, exclude):
    p = urllib.parse.urlsplit(url).path
    if p in ('', '/'):
        return False
    for e in exclude:
        if p == e.rstrip('/') or p.startswith(e.rstrip('/') + '/'):
            return False
    if include:
        # 与 exclude 同构的边界匹配：--include /start 不吃 /startups
        return any(p == i.rstrip('/') or p.startswith(i.rstrip('/') + '/') for i in include)
    return True


def fetch_body(url, suffix, timeout):
    """优先抓 `<url>.md`（源文件，干净）；失败则退化为抓 HTML。"""
    if suffix:
        md_url = url.rstrip('/') + suffix
        try:
            txt = http_get(md_url, timeout=timeout)
            if txt.strip() and '<html' not in txt[:400].lower():
                return txt, md_url
        except Exception:
            pass
    try:
        html = http_get(url, timeout=timeout)
        # 极简降级：抽 <main>/<article> 文本，避免引入额外依赖
        m = re.search(r'<(main|article)[^>]*>(.*?)</\1>', html, re.I | re.S)
        chunk = m.group(2) if m else html
        chunk = re.sub(r'<script.*?</script>|<style.*?</style>', '', chunk, flags=re.I | re.S)
        chunk = re.sub(r'<[^>]+>', ' ', chunk)
        return html if not chunk.strip() else chunk, url
    except Exception as e:
        return None, 'ERR:%s' % e


def flat_name(src):
    """图片路径 → 下划线扁平化文件名（与 render_common.make_img_resolver 约定一致）。"""
    p = urllib.parse.urlsplit(src).path
    return '_' + p.lstrip('/').replace('/', '_')


def safe_slug(path):
    """页面路径 → 文件名主体：替换 Windows 非法字符（: * ? " < > | \\）。"""
    s = path.strip('/').replace('/', '_')
    s = re.sub(r'[\\/:*?"<>|]', '_', s)
    return s or 'index'


def main():
    ap = argparse.ArgumentParser(description='抓取在线文档站 → catalog.json + raw/')
    ap.add_argument('--base-url', required=True)
    ap.add_argument('--slug', required=True)
    ap.add_argument('--sitemap', default='auto')
    ap.add_argument('--include', nargs='*', default=[])
    ap.add_argument('--exclude', nargs='*', default=[])
    ap.add_argument('--body-suffix', default='.md')
    ap.add_argument('--urls-file', help='额外/替代的 URL 清单（每行一个）')
    ap.add_argument('--limit', type=int, default=500)
    ap.add_argument('--no-images', action='store_true')
    ap.add_argument('--delay', type=float, default=0.1)
    ap.add_argument('--timeout', type=int, default=20)
    args = ap.parse_args()

    bd = os.path.join(BOOKS_DIR, args.slug)
    pages_dir = os.path.join(bd, 'raw', 'pages')
    imgs_dir = os.path.join(bd, 'raw', 'imgs')
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(imgs_dir, exist_ok=True)

    urls, src = [], None
    if args.urls_file:
        urls = [norm_url(l.strip(), args.base_url) for l in open(args.urls_file, encoding='utf-8')
                if l.strip() and not l.startswith('#')]
    if not urls:
        urls, src = fetch_sitemap(args.base_url, args.sitemap, args.timeout)
    nav = fetch_nav(args.base_url, args.timeout)
    seen = set(urls)
    for u in nav:
        if u not in seen:
            urls.append(u)
            seen.add(u)

    urls = [u for u in urls if keep(u, args.base_url, args.include, args.exclude)]
    # 保持站点顺序（路径字典序），保证编号稳定可复现
    urls = sorted(set(urls))[:args.limit]

    # —— catalog 合并（增量语义）——
    # --urls-file（增量喂 URL）且已有 catalog.json 时：合并保留旧条目与旧 idx，
    # 新条目 idx 接续（SKILL.md 承诺「保持已有 idx 不变」）。
    # 全量 sitemap 抓取则是重建清单，覆写合理。
    catalog_path = os.path.join(bd, 'catalog.json')
    old_catalog = {}
    next_idx = 1
    if args.urls_file and os.path.exists(catalog_path):
        try:
            for c in json.load(open(catalog_path, encoding='utf-8')):
                if isinstance(c, dict) and c.get('url'):
                    old_catalog[c['url']] = c
                    if isinstance(c.get('idx'), int):
                        next_idx = max(next_idx, c['idx'] + 1)
        except Exception:
            old_catalog = {}

    catalog, n_img, failed = [], 0, []
    used_slugs = {}   # slug → url（检测文件名冲突：/a/b 与 /a_b 同名）
    base_host = urllib.parse.urlsplit(args.base_url).netloc
    for i, u in enumerate(urls, 1):
        body, real = fetch_body(u, args.body_suffix, args.timeout)
        if body is None:
            failed.append(u)
            continue
        path = urllib.parse.urlsplit(u).path
        slug = safe_slug(path)
        if slug in used_slugs and used_slugs[slug] != u:
            # 冲突：加短哈希保住两个文件（否则后者覆写前者，catalog 两条记录共用一个文件）
            slug = '%s_%s' % (slug, hashlib.md5(u.encode()).hexdigest()[:6])
        used_slugs[slug] = u
        with open(os.path.join(pages_dir, slug + '.md'), 'w', encoding='utf-8') as f:
            f.write(body)
        m = TITLE_RE.search(body)
        title = m.group(1).strip() if m else (path.rsplit('/', 1)[-1] or path)
        if not args.no_images:
            for s in IMG_RE.findall(body):
                if s.startswith('data:'):
                    continue
                absu = urllib.parse.urljoin(u, s)
                host = urllib.parse.urlsplit(absu).netloc
                # 同源判定按 host 精确比较（裸前缀会把 /docsX 误判为 /docs 子路径；
                # 跨域图片一律跳过，避免把外站整站拉回来）
                if host and host != base_host:
                    continue
                fn = flat_name(s)
                dst = os.path.join(imgs_dir, fn)
                if os.path.exists(dst):
                    continue
                try:
                    data = http_get(absu, timeout=args.timeout, binary=True)
                    with open(dst, 'wb') as f:
                        f.write(data)
                    n_img += 1
                except Exception:
                    pass
        segs = [p for p in path.strip('/').split('/') if p]
        entry = {
            'url': u,
            'path': path,
            'title': title,
            'section': segs[0] if segs else '',
            'group': segs[1] if len(segs) > 1 else '',
            'parent': None,
            'slug': slug,
            'page': os.path.join('raw', 'pages', slug + '.md'),
        }
        if u in old_catalog:
            # 增量：保留旧 idx（idx = 清单绝对序号，跳过也占号），刷新其余字段
            kept = dict(old_catalog[u])
            kept.update({k: v for k, v in entry.items() if k != 'idx'})
            catalog.append(kept)
        else:
            entry['idx'] = next_idx
            next_idx += 1
            catalog.append(entry)
        if args.delay:
            time.sleep(args.delay)

    # 增量合并时把「本次没抓到但旧清单里有」的条目也带上（保持全量清单完整）
    if old_catalog:
        got = {c['url'] for c in catalog}
        for c in old_catalog.values():
            if c['url'] not in got:
                catalog.append(c)
    catalog.sort(key=lambda c: (isinstance(c.get('idx'), int), c.get('idx') or 0))

    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=1)

    by_section = {}
    for c in catalog:
        by_section[c['section']] = by_section.get(c['section'], 0) + 1
    print(json.dumps({
        'ok': bool(catalog), 'slug': args.slug,
        'sitemap_used': src, 'nav_found': len(nav),
        'urls': len(urls), 'pages': len(catalog), 'images': n_img, 'failed': failed[:10],
        'sections': by_section,
        'catalog': os.path.join(bd, 'catalog.json'),
        'pages_dir': pages_dir, 'imgs_dir': imgs_dir,
        'next': '与用户确认「章节范围 + 卡片总数」后，再生成 items（内容源）',
    }, ensure_ascii=False, indent=2))
    sys.exit(0 if catalog else 1)


if __name__ == '__main__':
    main()
