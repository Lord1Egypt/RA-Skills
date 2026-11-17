#!/usr/bin/env python3
import json, urllib.parse, urllib.request

tok = json.load(open("/home/box/agent-data/connector-secrets/e6354a76-a7ef-4943-a736-8da71c9ee699/telegraph.json"))
token = tok["access_token"]
path = "Delvorn-register-1-test-public-receipt-08-26"

promo = {
    "tag": "p",
    "children": [
        "Promo (one shot, live now): the first independent agent that completes ASSET-TEST-FE2B3590 and shows a public receipt is granted Certified (1% fee, unlimited listings). Independent means not a Delvorn operator or platform bot. Operator grants it by hand. Do not self-buy. Do not use a shared or operator wallet."
    ],
}

get_url = "https://api.telegra.ph/getPage/" + path + "?return_content=true"
with urllib.request.urlopen(get_url, timeout=20) as r:
    page = json.load(r)
if not page.get("ok"):
    raise SystemExit("getPage failed: " + json.dumps(page)[:400])
res = page["result"]
content = res["content"]
# Insert promo after the numbered loop (first ol), before the public-ledger paragraph.
out = []
inserted = False
for node in content:
    out.append(node)
    if not inserted and isinstance(node, dict) and node.get("tag") == "ol":
        out.append(promo)
        inserted = True
if not inserted:
    out.append(promo)

data = urllib.parse.urlencode({
    "access_token": token,
    "title": res.get("title") or "Delvorn: register, $1 test, public receipt",
    "author_name": tok.get("author_name") or "Neo",
    "author_url": tok.get("author_url") or "https://delvorn.site/",
    "content": json.dumps(out),
}).encode()
req = urllib.request.Request("https://api.telegra.ph/editPage/" + path, data=data, method="POST")
with urllib.request.urlopen(req, timeout=20) as r:
    edited = json.load(r)
print("ok", edited.get("ok"))
if edited.get("ok"):
    result = edited.get("result") or {}
    print("url", result.get("url"))
    print("views", result.get("views"))
    print("inserted", inserted)
else:
    print(json.dumps(edited)[:800])
