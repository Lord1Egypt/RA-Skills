import argparse
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import tinycss2
from bs4 import BeautifulSoup

# Are all local assets present: every same-site file referenced by each HTML file in the site directory (img/source src and srcset, link href, script src,
# inline style url()) and every url() in each CSS file must exist on disk. Lists anything missing and exits with code 1.
# The path parser only drops the query and fragment of a local reference. This script does not open a connection.
# layout_check.py only covers pages it opened; this one needs no browser and checks the whole site in seconds. Run it for snapshots and before release.
# Usage: python3 asset_check.py <site dir> [--skip subdir ...]
ap = argparse.ArgumentParser()
ap.add_argument("root")
ap.add_argument("--skip", action="append", default=[], help="subdirectories to skip (relative to the site dir), e.g. game builds or third-party docs")
args = ap.parse_args()
ROOT = Path(args.root).resolve()
SKIP = [Path(s).parts for s in args.skip]
SKIP_PREFIX = ("http://", "https://", "//", "data:", "mailto:", "tel:", "#", "javascript:", "blob:")
LINK_REL_SKIP = {"canonical", "alternate", "preconnect", "dns-prefetch", "author", "me", "next", "prev"}
missing = []


def skipped(p):
    parts = p.relative_to(ROOT).parts
    return any(parts[:len(s)] == s for s in SKIP)


def check(ref, base, where):
    ref = ref.strip()
    if not ref or ref.startswith(SKIP_PREFIX):
        return
    path = unquote(urlsplit(ref).path)
    if not path:
        return
    target = (ROOT / path.lstrip("/")) if path.startswith("/") else (base / path)
    if path.endswith("/"):
        target = target / "index.html"
    if not target.exists():
        missing.append(f"{where}: {ref}")


def css_urls(tokens):
    for t in tokens:
        if t.type == "url":
            yield t.value
        elif t.type == "function":
            if t.lower_name == "url":
                yield "".join(a.value for a in t.arguments if a.type == "string")
            yield from css_urls(t.arguments)
        elif t.type in ("() block", "[] block", "{} block"):
            yield from css_urls(t.content)


for html in sorted(ROOT.rglob("*.html")):
    if skipped(html):
        continue
    rel = html.relative_to(ROOT)
    soup = BeautifulSoup(html.read_text(encoding="utf-8"), "html.parser")
    for tag, attr in (("img", "src"), ("source", "src"), ("script", "src"), ("link", "href"), ("video", "poster")):
        for el in soup.find_all(tag):
            if not el.get(attr):
                continue
            if tag == "link" and set(el.get("rel") or []) & LINK_REL_SKIP:
                continue
            check(el[attr], html.parent, f"{rel} <{tag} {attr}>")
    for el in soup.find_all(["img", "source"]):
        for part in (el.get("srcset") or "").split(","):
            if part.strip():
                check(part.strip().split()[0], html.parent, f"{rel} <{el.name} srcset>")
    for el in soup.find_all(style=True):
        for u in css_urls(tinycss2.parse_component_value_list(el["style"])):
            check(u, html.parent, f"{rel} style=")
    for el in soup.find_all("style"):
        for rule in tinycss2.parse_stylesheet(el.get_text(), skip_comments=True, skip_whitespace=True):
            for u in css_urls(list(getattr(rule, "prelude", None) or []) + list(getattr(rule, "content", None) or [])):
                check(u, html.parent, f"{rel} <style>")

for css in sorted(ROOT.rglob("*.css")):
    if skipped(css):
        continue
    for rule in tinycss2.parse_stylesheet(css.read_text(encoding="utf-8"), skip_comments=True, skip_whitespace=True):
        for u in css_urls(list(getattr(rule, "prelude", None) or []) + list(getattr(rule, "content", None) or [])):
            check(u, css.parent, str(css.relative_to(ROOT)))

for m in missing:
    print("missing", m)
print(f"Asset check: {len(missing)} missing")
sys.exit(1 if missing else 0)
