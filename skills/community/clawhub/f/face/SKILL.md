---
name: Face
slug: face
version: 1.0.0
homepage: https://clawic.com/skills/face
description: "Put a human face on your agent with fast avatar shortlists, gender control, transparent options, and reusable profile links. Use when the user wants an avatar, profile face, or group image."
changelog: "Refines the positioning around putting a human face on the agent with faster avatar selection."
metadata: {"clawdbot":{"emoji":"👤","requires":{"bins":["curl","python3"]},"os":["linux","darwin","win32"]}}
---

# Put a Face on Your Agent

Use this skill to give an agent, persona, group, or Telegram surface a real human-looking face fast.

The job is simple:
- open a stable face listing URL
- extract a small shortlist of faces
- send the options to the user to choose
- if one is approved, reuse that link as the avatar or suggest saving it in identity

## Core Workflow

### 1. Start from the stable URL

Default to:

`https://generated.photos/faces/beautified/{gender}/young-adult`

Notes:
- `beautified` and `young-adult` are the best default for this use case
- gender is the main parameter that usually matters
- the site may also accept `.../young-adult/{gender}`, but the canonical form resolves to `.../{gender}/young-adult`

### 2. Only trust filters the site already exposes

From the page HTML, the route families that were verified as stable are:
- head pose: `front-facing`, `left-facing`, `right-facing`
- race: `asian-race`, `black-race`, `latino-race`, `white-race`
- eye color: `brown-eyes`, `grey-eyes`, `blue-eyes`, `green-eyes`
- hair color: `brown-hair`, `black-hair`, `blond-hair`
- hair length: `short`, `medium`, `long`
- emotion: `joy`, `neutral`

Do not invent deeper URL combinations from memory. If the user wants narrower filtering, open the base page and follow the exact links that page emits.

### 3. Extract faces from HTML before using a browser

The page already contains:
- `/face/...` detail links
- `data-image-id`
- `https://images.generated.photos/...` preview URLs

Use a direct fetch first. Return 3 to 6 options max.

```python
python3 - <<'PY'
import json
import re
from urllib.request import Request, urlopen

url = "https://generated.photos/faces/beautified/female/young-adult"
raw = urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"})).read().decode()

cards = re.findall(
    r'href="(/face/[^"]+)".*?data-image-id="([^"]+)".*?src="(https://images.generated.photos[^"]+)"',
    raw,
    re.S,
)
transparent = {
    image_id: thumb.replace("\\u002F", "/")
    for image_id, thumb in re.findall(
        r'id:"([^"]+)".*?transparent:\{thumb_url:"([^"]+)"',
        raw,
    )
}

for n, (detail, image_id, thumb) in enumerate(cards[:6], 1):
    print(json.dumps({
        "n": n,
        "detail": "https://generated.photos" + detail,
        "thumb": thumb,
        "transparent": transparent.get(image_id),
    }))
PY
```

### 4. Treat background as extraction, not routing

Do not model background as a clean route parameter.

What was verified:
- the page UI shows a background area
- the route itself does not expose a simple stable public background parameter
- transparent versions appear in embedded data as `transparent.thumb_url`

Rule:
- if the user wants a transparent avatar, prefer `transparent.thumb_url`
- if the user wants a bigger preview, open the chosen detail page and use the 512px `og:image` or `twitter:image`

### 5. Always keep the user in the loop

Default output should be:
- 3 to 6 numbered options
- one normal preview per option
- transparent preview too when available
- the detail page link

Do not auto-pick unless the user asks.

### 6. Reuse the chosen face properly

Once the user chooses one:
- propose using it as the avatar for the agent, group, Telegram profile, or similar
- if it is their long-term face, suggest storing the chosen link in identity
- keep the detail page link, not just the image preview URL

## Recommended Response Shape

When you answer, keep it compact:

```text
I found 4 options for your agent face.

1. Option A
   Detail: ...
   Preview: ...
   Transparent: ...

2. Option B
   Detail: ...
   Preview: ...
   Transparent: ...

Tell me which one you want and I’ll prepare it as the avatar.
```

## Common Mistakes

- guessing URL variants instead of following the page's real filters
- trying to control background through the route
- showing too many faces at once
- saving only the preview URL instead of the detail link
- changing an avatar without explicit approval

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://generated.photos | Filter path segments and face detail page requests | Find faces and open detail pages |
| https://images.generated.photos | Image GET requests only | Preview and transparent preview retrieval |

No other data is sent externally.
