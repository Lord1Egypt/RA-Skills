"""
🛠️ axiom-markdown-link-auditor — Markdown Link Checker
========================================================

⚠️ LIMITATIONS CONNUES :
- Pas de support JS-rendered pages
- Pas de validation des liens d'ancrage internes (#[...])
- HTTPS check ne suit pas les redirects (HEAD seulement)

AUDITE LES LIENS DANS UN FICHIER MARKDOWN
"""

import re
import sys
import urllib.request
import urllib.error


# Markdown link pattern: [text](url)
LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
# Markdown image pattern: ![alt](url)
IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
# Bare URLs
BARE_URL_PATTERN = re.compile(r"https?://[^\s<>\"']+")


def extract_links(markdown_text: str) -> list:
    """
    Extract all links from markdown text.

    Returns list of dicts: {type, text, url, line}
    """
    links = []
    lines = markdown_text.split("\n")

    for line_num, line in enumerate(lines, 1):
        # Find [text](url) patterns
        for match in LINK_PATTERN.finditer(line):
            text, url = match.group(1), match.group(2)
            # Skip images
            if line[max(0, match.start() - 1):match.start()] == "!":
                continue
            links.append({
                "type": "link",
                "text": text,
                "url": url,
                "line": line_num,
            })

        # Find ![alt](url) for images
        for match in IMAGE_PATTERN.finditer(line):
            alt, url = match.group(1), match.group(2)
            links.append({
                "type": "image",
                "text": alt,
                "url": url,
                "line": line_num,
            })

        # Find bare URLs
        for match in BARE_URL_PATTERN.finditer(line):
            url = match.group(0)
            # Skip if already captured in [text](url)
            already_captured = any(link["url"] in url or url in link["url"] for link in links if link["line"] == line_num)
            if not already_captured:
                links.append({
                    "type": "bare_url",
                    "text": url,
                    "url": url,
                    "line": line_num,
                })

    return links


def check_url(url: str, timeout: int = 5) -> dict:
    """
    Check a single URL via HEAD request.

    Returns dict with: url, status, ok, error
    """
    # Skip non-HTTP schemes
    if not url.startswith(("http://", "https://")):
        return {
            "url": url,
            "status": None,
            "ok": None,
            "skipped": True,
            "reason": f"Non-HTTP scheme: {url.split(':')[0]}",
        }

    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "axiom-markdown-link-auditor/0.1")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {
                "url": url,
                "status": resp.status,
                "ok": 200 <= resp.status < 400,
                "skipped": False,
            }
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "ok": False, "skipped": False, "error": str(e)}
    except urllib.error.URLError as e:
        return {"url": url, "status": None, "ok": False, "skipped": False, "error": str(e)}
    except Exception as e:
        return {"url": url, "status": None, "ok": False, "skipped": False, "error": str(e)}


def audit(markdown_text: str, check_remote: bool = False, timeout: int = 5) -> dict:
    """
    Audit a markdown text for links.

    Returns dict with: total, by_type, broken (if check_remote), links
    """
    links = extract_links(markdown_text)

    by_type = {}
    for link in links:
        t = link["type"]
        by_type[t] = by_type.get(t, 0) + 1

    result = {
        "total": len(links),
        "by_type": by_type,
        "links": links,
    }

    if check_remote:
        broken = []
        for link in links:
            url = link["url"]
            if not url.startswith(("http://", "https://")):
                continue
            check = check_url(url, timeout=timeout)
            if not check.get("ok") and not check.get("skipped"):
                broken.append({**link, **check})
        result["broken"] = broken
        result["broken_count"] = len(broken)

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="axiom-markdown-link-auditor ")
    parser.add_argument("file", nargs="?", help="Markdown file to audit")
    parser.add_argument("--check-remote", action="store_true", help="Check HTTP status (slow)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if not args.file:
        # Demo
        demo_md = """# Demo

Check [GitHub](https://github.com) and [broken](https://this-domain-does-not-exist-abc123.com).

![logo](https://example.com/logo.png)

Also see https://example.org for more.
"""
        result = audit(demo_md, check_remote=False)
        if args.json:
            import json
            print(json.dumps(result, indent=2))
        else:
            print(f"Total links: {result['total']}")
            for t, count in result["by_type"].items():
                print(f"  {t}: {count}")
            print()
            for link in result["links"]:
                print(f"  L{link['line']:>3} {link['type']:<10} {link['url']}")
        return 0

    with open(args.file, "r", encoding="utf-8") as f:
        md_text = f.read()
    result = audit(md_text, check_remote=args.check_remote)

    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        print(f"Total links: {result['total']}")
        for t, count in result["by_type"].items():
            print(f"  {t}: {count}")
        if args.check_remote:
            print(f"Broken: {result.get('broken_count', 0)}")
            for b in result.get("broken", []):
                print(f"  ❌ L{b['line']} {b['url']} ({b.get('error', b.get('status'))})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
