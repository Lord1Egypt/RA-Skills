# Oxylabs Dedicated Datacenter Proxies — connection cheat sheet

## Correct proxy URL format

For **Oxylabs Dedicated Datacenter Proxies (DDC, self-service)**, the proxy URL is:

```
http://USERNAME:PASSWORD@ddc.oxylabs.io:PORT
```

- **Entry point**: `ddc.oxylabs.io` (NOT direct IP, NOT `pr.oxylabs.io`)
- **Port**: `8001` and up (each port = one assigned IP)
- Username: the proxy user created in Oxylabs dashboard (e.g. `yourname_AB12C`)

**Common mistake**: trying to connect to the assigned IP directly (e.g. `45.73.183.199:8001`). Oxylabs explicitly states: *"you will not directly access your IPs"*. Use the entry point domain, not the IP.

`proxies.json` example for 3 DDC ports:

```json
{
  "proxies": [
    "http://user-ACCOUNT_ID:PASSWORD@ddc.oxylabs.io:8001",
    "http://user-ACCOUNT_ID:PASSWORD@ddc.oxylabs.io:8002",
    "http://user-ACCOUNT_ID:PASSWORD@ddc.oxylabs.io:8003"
  ]
}
```

## Response code quick reference (from Oxylabs docs)

| Code | Meaning | What to do |
|------|---------|------------|
| 400 | Bad request format | Check the URL format above |
| 403 | **Restricted target** | The site (e.g. amazon.com) is on Oxylabs' restricted list for this proxy product. Switch proxy product (e.g. ISP Proxies) or use Web Scraper API instead |
| 407 | Auth failed or IP not whitelisted | Wrong username/password, or you switched VPS and didn't re-whitelist the new exit IP |
| 429 | Thread / concurrent session limit exceeded | Slow down, or buy more bandwidth |
| 503 | **DNS failure to target** | Target site unreachable from proxy. Test target directly to confirm |
| 504 | Proxy timeout (60s) | Target is slow; retry or extend timeout |

## Verifying proxy works (in 30 seconds)

Before scraping, test the proxy chain with a simple reachability check:

```bash
curl -x ddc.oxylabs.io:8001 -U "USERNAME:PASSWORD" http://ip.oxylabs.io/location
```

- **200 + JSON with your assigned IP** → proxy works
- **503** → either wrong credentials OR target DNS issue (rare; mostly 503 = restricted target like Amazon)
- **No route to host / connection refused** → VPS can't reach Oxylabs' datacenter IP range (likely GFW / VPS provider blocking 45.x.x.x). Use the entry point domain `ddc.oxylabs.io` instead, which uses DNS to find a routable IP

## When DDC doesn't work for your target (Amazon specifically)

Amazon aggressively blocks datacenter ASN ranges. If you get HTTP 200 but the page says *"Sorry! Something went wrong!"* — that's Amazon's soft-block, not a proxy config error. The proxy is working, but Amazon has flagged the IP.

**What works for Amazon** (in order of cost):
1. **Oxylabs ISP Proxies** (`isn.oxylabs.io` or `pr.oxylabs.io:8001`) — same company, residential-grade IPs, passes Amazon
2. **Oxylabs Web Scraper API** (HTTP POST, not a proxy) — `https://realtime.oxylabs.io/v1/queries` with `source: "amazon_search"` etc. — no scraping code needed, ~$1.50/1K requests
3. **Other providers' ISP pools** (Smartproxy, IPIDEA, Bright Data ISP)

DDC is the cheapest product but is fundamentally the wrong tool for Amazon-scale scraping.

## Rotating through multiple proxies

In `proxies.json` you can list multiple URLs. The `amazon_handler.js` script in this skill auto-rotates through them per request and falls back on failure. No extra config needed beyond a JSON array.
