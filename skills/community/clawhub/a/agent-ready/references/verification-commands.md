# Verification Commands

All curl and shell commands used across the 9-item checklist, collected in one place
for quick reference. Run these as part of Gate 4 after each step — do not rely on API
success responses alone.

## After item 1: Trust anchor pages

Check each page returns real content and a 200:

```
curl -s -o /dev/null -w "%{http_code}" -L https://yourdomain.com/about/
curl -s -o /dev/null -w "%{http_code}" -L https://yourdomain.com/contact/
curl -s -o /dev/null -w "%{http_code}" -L https://yourdomain.com/privacy/
```

Confirm content length (should be well over 500 chars of text):

```
curl -s -L https://yourdomain.com/about/ | python3 -c "
import sys, re
h = sys.stdin.read()
text = re.sub(r'<[^>]+>', '', h)
text = re.sub(r'\s+', ' ', text).strip()
print(len(text), 'text chars')
"
```

## After item 2: JSON-LD schema

Confirm the script block is present in the page head:

```
curl -s -L https://yourdomain.com/ | grep -o 'application/ld+json'
```

Confirm the full block content:

```
curl -s -L https://yourdomain.com/ | python3 -c "
import sys, re
h = sys.stdin.read()
blocks = re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', h, re.DOTALL)
for b in blocks:
    print(b.strip())
    print('---')
"
```

Then validate at: https://search.google.com/test/rich-results (paste live URL)

## After item 3: llms.txt

Confirm the file is reachable and returns content:

```
curl -s -L https://yourdomain.com/llms.txt/
```

Validate at: https://llmstxt.cloud (paste live URL)

## After item 5 investigation: Content without JavaScript

Check raw HTML character count and H1 presence:

```
curl -s -L https://yourdomain.com/ | python3 -c "
import sys, re
h = sys.stdin.read()
print(len(h), 'raw HTML chars')
text = re.sub(r'<[^>]+>', '', h)
text = re.sub(r'\s+', ' ', text).strip()
print(len(text), 'text-only chars')
print('H1 found' if '<h1' in h.lower() else 'NO H1 — investigate further')
"
```

## After item 7 investigation: Agent-friendly 404s

Confirm nonexistent paths return 404 (following redirects):

```
curl -s -o /dev/null -w "%{http_code}" -L https://yourdomain.com/this-path-does-not-exist-at-all
```

Expected: `404`. If `200` — real issue, investigate further. If a redirect that
resolves to `404` — correct, normal Ghost www-redirect behavior.

## General: check any redirect chain

```
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://yourdomain.com/any-path
```
