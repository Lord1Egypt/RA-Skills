import argparse
import time
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser(description='Wait with one browser page until the live HTML, stylesheets and scripts match the new-version strings.')
    ap.add_argument('url')
    ap.add_argument('--has', nargs='+', default=[])
    ap.add_argument('--gone', nargs='+', default=[])
    ap.add_argument('--timeout', type=float, default=1500)
    ap.add_argument('--every', type=float, default=15)
    ap.add_argument('--settle', type=int, default=800)
    a = ap.parse_args()
    if not a.has and not a.gone:
        ap.error('give --has or --gone')
    if a.timeout < 0 or a.every <= 0 or a.settle < 0:
        ap.error('timeout and settle must not be negative; every must be positive')
    parts = urlsplit(a.url)
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if key != 'v']
    start = time.monotonic()
    deadline = start + a.timeout
    missing, present = list(a.has), list(a.gone)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        round_number = 0
        while True:
            round_number += 1
            url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query + [('v', str(round_number))]), parts.fragment))
            page.goto(url, wait_until='load')
            page.wait_for_timeout(a.settle)
            documents = [(page.url, page.content())]
            urls = page.evaluate("""() => [...new Set([
                ...[...document.styleSheets].map(s => s.href),
                ...[...document.scripts].map(s => s.src)
            ].filter(Boolean))]""")
            for resource_url in urls:
                response = page.request.get(resource_url)
                if not response.ok:
                    raise RuntimeError(f'Resource request failed: {response.status} {resource_url}')
                documents.append((resource_url, response.text()))
                response.dispose()
            found = {needle: [path for path, body in documents if needle in body] for needle in a.has}
            missing = [needle for needle, paths in found.items() if not paths]
            present = [needle for needle in a.gone if any(needle in body for _, body in documents)]
            elapsed = time.monotonic() - start
            if not missing and not present:
                print(f'New version is live: round {round_number}, waited {elapsed:.1f}s')
                for needle, paths in found.items():
                    print(f"  {needle}: {', '.join(paths)}")
                browser.close()
                return 0
            print(f'Round {round_number}, waited {elapsed:.1f}s, missing: {missing}, still present: {present}', flush=True)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            # report right at the deadline instead of sending another full round of requests
            time.sleep(min(a.every, remaining))
            if time.monotonic() >= deadline:
                break
        browser.close()
    print(f'Timed out after {time.monotonic() - start:.1f}s; missing {missing}; still present {present}')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
