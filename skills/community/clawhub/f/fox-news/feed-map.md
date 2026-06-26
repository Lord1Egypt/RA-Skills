# Feed Map - Fox News Desk

Use official Fox-owned surfaces first.

## Primary Surfaces

| Surface | URL | Use When | Notes |
|---------|-----|----------|-------|
| Latest feed | `https://moxie.foxnews.com/google-publisher/latest.xml` | User wants a fast top-line sweep | Broadest Fox headline mix |
| Politics feed | `https://moxie.foxnews.com/google-publisher/politics.xml` | Politics-specific monitoring | Better than homepage filtering |
| U.S. page | `https://www.foxnews.com/us` | Domestic news requests | Use page routing when RSS is too broad |
| World page | `https://www.foxnews.com/world` | International coverage | Use before general search |
| Opinion page | `https://www.foxnews.com/opinion` | User explicitly wants columnist or editorial coverage | Keep separate from straight-news summaries |
| Video page | `https://www.foxnews.com/video` | User wants clips, segments, or show highlights | Good fallback when live TV is gated |
| Live page | `https://www.foxnews.com/live-news` | Ongoing events and rolling updates | Best for fast-changing stories |
| Apps and products | `https://www.foxnews.com/apps-products/index.html` | App or device workflow questions | Use with help pages for support checks |

## Routing Rules

1. Use one surface first, not three at once.
2. Prefer RSS for deterministic headline capture and page routes for live or editorial context.
3. Keep `opinion` and `video` requests explicit so they do not leak into general briefings.

## Fast Shell Checks

When shell access is available, these are the fastest low-risk probes:

```bash
curl -s https://moxie.foxnews.com/google-publisher/latest.xml | head
curl -s https://moxie.foxnews.com/google-publisher/politics.xml | head
curl -s https://www.foxnews.com/live-news | head
```

For quick title extraction from RSS:

```bash
python3 - <<'PY'
import xml.etree.ElementTree as ET
import urllib.request

url = "https://moxie.foxnews.com/google-publisher/latest.xml"
root = ET.fromstring(urllib.request.urlopen(url).read())
for item in root.findall(".//item")[:5]:
    print(item.findtext("title", "").strip())
PY
```

Use commands only to inspect public pages and feeds. Do not automate credentialed playback or account flows.
