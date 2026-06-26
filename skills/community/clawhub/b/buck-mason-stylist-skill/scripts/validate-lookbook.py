#!/usr/bin/env python3
"""Validate a lookbook against references/acceptance-checklist.md.

Two modes:

  --dir <path>   Run local checks (L1-L10) against a deploy directory.
  --url <url>    Run deployed checks (D1-D6) against a live URL.

Both modes can be passed in one invocation (--dir + --url runs everything).

Exit codes:
  0  all checks passed
  1  one or more local checks failed
  2  one or more deployed checks failed (and locals were either skipped or passed)

Warnings (W*) print to stderr with WARN: prefix; never affect exit code.
"""
import argparse, html, json, pathlib, re, sys, subprocess, urllib.parse

ap = argparse.ArgumentParser(description="Validate a lookbook artifact + deploy.")
ap.add_argument("--dir", type=pathlib.Path, help="Local deploy directory")
ap.add_argument("--url", type=str,         help="Deployed page URL (e.g. https://<project>.pages.dev/)")
args = ap.parse_args()

if not args.dir and not args.url:
    print("error: specify --dir or --url (or both)", file=sys.stderr)
    sys.exit(2)

failures = []
warnings = []

def ok(check, msg):     print(f"  ✓ {check}: {msg}")
def fail(check, msg):   print(f"  ✗ {check}: {msg}", file=sys.stderr); failures.append(check)
def warn(check, msg):   print(f"  WARN {check}: {msg}", file=sys.stderr); warnings.append(check)

# ── Local checks ────────────────────────────────────────────────────────────

local_failed = False
if args.dir:
    print(f"\n=== local checks against {args.dir} ===")
    if not args.dir.is_dir():
        fail("L1", f"deploy dir not found: {args.dir}"); sys.exit(1)
    index = args.dir / "index.html"
    html_text = ""
    # L1
    if not index.exists():
        fail("L1", "index.html missing")
    elif index.stat().st_size < 4 * 1024:
        fail("L1", f"index.html only {index.stat().st_size} bytes (< 4 KB; suspicious)")
    else:
        ok("L1", f"index.html present ({index.stat().st_size} bytes)")
        html_text = index.read_text()

    if html_text:
        # L2 — every product link is on-brand and looks complete
        product_links = re.findall(r'href="(https://www\.buckmason\.com/products/[^"#?]+)"', html_text)
        if not product_links:
            fail("L2", "no buckmason.com/products/ links found")
        else:
            ok("L2", f"{len(product_links)} product link(s) on-brand")

        # L3 — prices appear in piece blocks
        piece_blocks = re.findall(r'<label[^>]+class="piece"[^>]*>(.*?)</label>', html_text, re.S)
        if not piece_blocks:
            fail("L3", "no .piece blocks found (expected at least one)")
        else:
            missing_price = [i for i, b in enumerate(piece_blocks) if not re.search(r'\$\d+', b)]
            if missing_price:
                fail("L3", f"{len(missing_price)} piece block(s) missing price")
            else:
                ok("L3", f"all {len(piece_blocks)} piece block(s) have price")

            # L4 — stock lines per piece
            missing_stock = [i for i, b in enumerate(piece_blocks)
                             if not re.search(r'(In stock|Low \(\d+\)|Low stock|Out of stock|Out)', b)]
            if missing_stock:
                fail("L4", f"{len(missing_stock)} piece block(s) missing stock line")
            else:
                ok("L4", "stock lines present on every piece")

            # L8 — html-cart per-piece data attrs (only when piece blocks contain checkboxes)
            has_checkboxes = '<input type="checkbox"' in html_text
            if has_checkboxes:
                required = ["data-name", "data-size", "data-sku", "data-qty", "data-price-cents"]
                missing_attrs = [a for a in required
                                 if not re.search(rf'<input[^>]+{re.escape(a)}=', html_text)]
                if missing_attrs:
                    fail("L8", f"checkbox data-attrs missing: {missing_attrs}")
                else:
                    ok("L8", "all checkbox data-attrs present")

        # L5 — AI disclosure (only required if any look hero references a generated image)
        has_ai = bool(re.search(r'<img[^>]+src="look\d+\.(jpg|png)"', html_text))
        if has_ai:
            if re.search(r'(AI[- ]generated|AI try-on)', html_text, re.I):
                ok("L5", "AI disclosure present")
            else:
                fail("L5", "look hero present but no AI disclosure copy")
        else:
            ok("L5", "no AI hero — disclosure not required")

        # L6 — OG meta tags absolute (no placeholder leftovers)
        og_url   = re.search(r'<meta property="og:url"[^>]*content="([^"]+)"',   html_text)
        og_image = re.search(r'<meta property="og:image"[^>]*content="([^"]+)"', html_text)
        twitter  = re.search(r'<meta name="twitter:image"[^>]*content="([^"]+)"', html_text)
        bad = []
        for label, m in [("og:url", og_url), ("og:image", og_image), ("twitter:image", twitter)]:
            if not m:
                bad.append(f"{label} missing")
            elif not m.group(1).startswith("https://"):
                bad.append(f"{label} not absolute: {m.group(1)}")
            elif "{{" in m.group(1):
                bad.append(f"{label} has unsubstituted placeholder: {m.group(1)}")
        if bad:
            fail("L6", "; ".join(bad))
        else:
            ok("L6", "og:url + og:image + twitter:image all absolute")

        # L7 — og.jpg present + reasonably sized
        og = args.dir / "og.jpg"
        if not og.exists():
            fail("L7", "og.jpg missing")
        elif og.stat().st_size > 500 * 1024:
            warn("W-L7", f"og.jpg is {og.stat().st_size//1024} KB (>500 KB; may slow unfurls)")
            ok("L7", f"og.jpg present ({og.stat().st_size//1024} KB)")
        else:
            ok("L7", f"og.jpg present ({og.stat().st_size//1024} KB)")

        # L10 — no broken inline references
        broken = []
        for m in re.finditer(r'(src|href|data-fullsize)="(\s*|#)"', html_text):
            broken.append(m.group(0))
        if broken:
            fail("L10", f"{len(broken)} empty src/href/data-fullsize attribute(s): {broken[:3]}")
        else:
            ok("L10", "no empty src/href/data-fullsize")

    local_failed = bool(failures)

# ── Deployed checks ─────────────────────────────────────────────────────────

deployed_failed = False
if args.url:
    print(f"\n=== deployed checks against {args.url} ===")
    base = args.url if args.url.endswith("/") else args.url + "/"

    def head(url):
        r = subprocess.run(["curl", "-sIL", "--max-time", "15", url], capture_output=True, text=True)
        return r.stdout

    def get(url):
        r = subprocess.run(["curl", "-sSL", "--max-time", "15", url], capture_output=True, text=True)
        return r.stdout

    # D1
    h = head(base)
    if "200" in h.split("\n")[0] or " 200 " in h.split("\n")[0]:
        ok("D1", f"{base} → 200")
    else:
        fail("D1", f"page returned: {h.split(chr(10))[0]}")

    # D2
    og_url = base + "og.jpg"
    h = head(og_url)
    first = h.split("\n")[0] if h else ""
    ctype = next((l for l in h.split("\n") if l.lower().startswith("content-type:")), "")
    if "200" in first and "image/jpeg" in ctype.lower():
        ok("D2", f"{og_url} → 200 image/jpeg")
    else:
        fail("D2", f"og.jpg head: {first} / {ctype.strip()}")

    # D3 — look<N>.jpg presence (multi-file deploys)
    body = get(base)
    look_files = sorted(set(re.findall(r'src="(look\d+\.jpg)"', body)))
    for lf in look_files:
        h = head(base + lf)
        if "200" in (h.split("\n")[0] if h else ""):
            ok(f"D3:{lf}", "200")
        else:
            fail(f"D3:{lf}", f"head: {(h.split(chr(10))[0]) if h else 'no response'}")

    # D4 — meta tags survived
    expected_props = ["og:type", "og:title", "og:description", "og:url", "og:image",
                      "twitter:card", "twitter:title", "twitter:image"]
    missing = [p for p in expected_props if f'property="{p}"' not in body and f'name="{p}"' not in body]
    if missing:
        fail("D4", f"meta tags missing on deployed page: {missing}")
    else:
        ok("D4", "all OG/Twitter meta tags survived deploy")

    # D5 — resolved og:url + og:image are themselves reachable
    og_url_live = re.search(r'<meta property="og:url"[^>]*content="([^"]+)"', body)
    og_img_live = re.search(r'<meta property="og:image"[^>]*content="([^"]+)"', body)
    for label, m in [("og:url", og_url_live), ("og:image", og_img_live)]:
        if not m:
            fail(f"D5:{label}", "tag missing in served HTML")
            continue
        ref = m.group(1)
        h = head(ref)
        if "200" in (h.split("\n")[0] if h else ""):
            ok(f"D5:{label}", f"{ref} → 200")
        else:
            fail(f"D5:{label}", f"{ref} not reachable: {(h.split(chr(10))[0]) if h else 'no response'}")

    # D6 — verify with a Facebook-like User-Agent that the meta tags still come back
    r = subprocess.run(
        ["curl", "-sSL", "--max-time", "15", "-A", "facebookexternalhit/1.1", base],
        capture_output=True, text=True,
    )
    if 'property="og:image"' in r.stdout:
        ok("D6", "og tags visible to facebookexternalhit/1.1 UA")
    else:
        fail("D6", "og tags not visible to fb-style UA — unfurl will fail")

    # W1 — public-by-URL warning (always true for these hosts)
    if any(host in base for host in [".pages.dev", ".netlify.app", ".vercel.app", ".surge.sh", "0x0.st", "gist.github"]):
        warn("W1", f"deployed publicly to {base} — anyone with the URL can view")

    deployed_failed = any(c.startswith("D") for c in failures)

# ── Summary ────────────────────────────────────────────────────────────────

print()
if not failures:
    print(f"✅ all checks passed ({len(warnings)} warning(s))")
    sys.exit(0)
elif local_failed:
    print(f"❌ local check failed: {[c for c in failures if c.startswith('L')]}")
    sys.exit(1)
elif deployed_failed:
    print(f"❌ deployed check failed: {[c for c in failures if c.startswith('D')]}")
    sys.exit(2)
else:
    print(f"❌ unspecified failure: {failures}")
    sys.exit(1)
