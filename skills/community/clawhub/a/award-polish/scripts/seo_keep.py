import argparse
import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup


def html_fields(content):
    soup = BeautifulSoup(content, 'html.parser')
    def text(selector):
        el = soup.select_one(selector)
        return el.get_text(' ', strip=True) if el else None
    def attr(selector, key):
        el = soup.select_one(selector)
        return el.get(key) if el else None
    types = []
    def visit(value):
        if isinstance(value, list):
            for item in value:
                visit(item)
        elif isinstance(value, dict):
            kind = value.get('@type', [])
            types.extend(kind if isinstance(kind, list) else [kind])
            for key, item in value.items():
                if key != '@type':
                    visit(item)
    for script in soup.select('script[type="application/ld+json"]'):
        visit(json.loads(script.string if script.string is not None else script.get_text()))
    fields = {'title': text('title'),
              'description': attr('meta[name="description"]', 'content'),
              'canonical': attr('link[rel="canonical"]', 'href'),
              'hreflang': sorted(f"{el.get('hreflang')}={el.get('href')}" for el in soup.select('link[hreflang]')),
              'robots': attr('meta[name="robots"]', 'content'),
              'jsonld_types': sorted(types), 'h1': text('h1'), 'lang': attr('html', 'lang')}
    for prop in ('og:title', 'og:description', 'og:image'):
        fields[prop] = attr(f'meta[property="{prop}"]', 'content')
    fields['twitter:card'] = attr('meta[name="twitter:card"],meta[property="twitter:card"]', 'content')
    return fields


def under(base, path):
    # append the page path to base: urljoin drops a base subpath such as http://localhost:8790/a/
    return base.rstrip('/') + '/' + path.lstrip('/')


def page_fields(response):
    return {'status': response.status_code, **html_fields(response.content)}


def sitemap_paths(session, url, count):
    response = session.get(url, timeout=30)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    local = root.tag.rsplit('}', 1)[-1]
    paths = []
    for node in root:
        loc = next((child.text for child in node if child.tag.rsplit('}', 1)[-1] == 'loc'), None)
        if loc is None:
            continue
        if local == 'sitemapindex':
            paths.extend(sitemap_paths(session, urljoin(url, loc), count - len(paths)))
        else:
            parts = urlsplit(loc)
            paths.append(urlunsplit(('', '', parts.path or '/', parts.query, '')))
        if len(paths) >= count:
            break
    return paths[:count]


def baseline_path(value):
    """Return the --dump file, which must stay inside the repo or the working directory.

    The path is relative. Absolute paths and ``..`` segments are refused, including
    after resolving the working directory. When this command is run inside a git
    checkout, a path inside that checkout is also accepted.
    """
    if not isinstance(value, str) or not value.strip() or "\0" in value or "\n" in value or "\r" in value:
        sys.exit("--dump must be a plain relative path inside the repo or the working directory")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        sys.exit("--dump must be a plain relative path inside the repo or the working directory; absolute paths and .. are refused")
    cwd = Path.cwd().resolve()
    target = (cwd / path).resolve()
    roots = [cwd]
    for candidate in (cwd, *cwd.parents):
        if (candidate / ".git").exists():
            roots.append(candidate.resolve())
            break
    if not any(_inside(target, root) for root in roots):
        sys.exit("--dump must stay inside the repo or the working directory")
    return target


def _inside(path, root):
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def main():
    ap = argparse.ArgumentParser(description='Compare SEO fields of the live and new pages plus given files; any difference exits with code 1.')
    ap.add_argument('--base', required=True)
    ap.add_argument('--new', required=True)
    ap.add_argument('--pages', nargs='+', default=[])
    ap.add_argument('--sitemap', type=int)
    ap.add_argument('--files', nargs='+', default=[])
    ap.add_argument('--dump', help='relative path inside the repo or working directory for the search-baseline JSON; absolute paths and .. are refused')
    a = ap.parse_args()
    if not a.pages and not a.sitemap:
        ap.error('give --pages and/or a positive --sitemap')
    if a.sitemap is not None and a.sitemap <= 0:
        ap.error('--sitemap needs a positive integer')
    dump_to = baseline_path(a.dump) if a.dump else None
    differences = 0
    baseline = {}
    with requests.Session() as session:
        pages = list(dict.fromkeys(a.pages + (sitemap_paths(session, under(a.base, 'sitemap.xml'), a.sitemap) if a.sitemap else [])))
        for path in pages:
            before = page_fields(session.get(under(a.base, path), timeout=30))
            after = page_fields(session.get(under(a.new, path), timeout=30))
            baseline[path] = before
            changed = [key for key in before if before[key] != after[key]]
            differences += len(changed)
            print(f"{'DIFF' if changed else 'OK'} {path}")
            for key in changed:
                print(f'  {key}: base={json.dumps(before[key], ensure_ascii=False)} new={json.dumps(after[key], ensure_ascii=False)}')
        for path in a.files:
            before = session.get(under(a.base, path), timeout=30)
            after = session.get(under(a.new, path), timeout=30)
            before.raise_for_status()
            after.raise_for_status()
            changed = before.content != after.content
            differences += int(changed)
            print(f"{'DIFF' if changed else 'OK'} file {path}")
            if changed:
                print(f'  bytes: base={before.content!r} new={after.content!r}')
    if dump_to is not None:
        dump_to.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        for path, fields in baseline.items():
            print(f'baseline {path}: ' + '; '.join(f'{k}={json.dumps(v, ensure_ascii=False)}' for k, v in fields.items()))
        print(f'Search baseline saved: {a.dump}')
    print(f'{len(pages)} pages, {differences} differences')
    return int(differences > 0)


if __name__ == '__main__':
    raise SystemExit(main())
