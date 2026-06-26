---
name: chatgpt-image-tailnet
description: Generate and download ChatGPT images through the remote Camoufox browser reachable over the tailnet, especially when residential/IP reputation matters more than the local host IP. Use this when you need to open chatgpt.com on the remote residential browser, submit a custom image prompt, wait for generation, and save or send back the resulting image without relying on a Tailscale exit node.
---

Use the remote Camoufox browser over its tailnet IP instead of changing the current machine's exit-node routing.

Default assumptions for this workspace:
- Preferred remote browser API: `http://100.89.48.48:9377`
- This is the residential/Türkiye browser path on `Inspiron-gnmd-1`
- ChatGPT image generation should happen inside that remote browser session
- Downloads should be captured from inside the browser context, not fetched directly from the local host

## Why this skill exists

- ChatGPT/Cloudflare-sensitive flows work better on the residential remote browser than on datacenter/server IPs.
- The reliable path is **remote browser over tailnet IP**, not **reconfiguring a Tailscale exit node for every task**.
- Generated image URLs may 403 when fetched from outside the logged-in browser context; trigger the download from inside the page and collect it through Camoufox downloads.

## Core workflow

1. Open `https://chatgpt.com/` on the remote Camoufox browser.
2. Switch to **Create an image** mode.
3. Type the user's custom prompt.
4. Submit and poll snapshots until a generated image appears.
5. Trigger a browser-context fetch/download from the page itself.
6. Read the downloaded file from `/tabs/:tabId/downloads` and save/send it.

## Script

Use the bundled helper:

```bash
python3 skills/chatgpt-image-tailnet/scripts/chatgpt_image_tailnet.py "your prompt here"
```

Optional flags:

```bash
python3 skills/chatgpt-image-tailnet/scripts/chatgpt_image_tailnet.py \
  "your prompt here" \
  --base http://100.89.48.48:9377 \
  --user lotfi \
  --session chatgpt-image-helper \
  --output /tmp/result.png \
  --timeout 180
```

## Important rules

- Prefer the remote tailnet Camoufox base over any local browser by default for this flow.
- Do **not** depend on Tailscale exit-node switching for normal operation.
- Keep the prompt as a script input, not as a baked-in macro.
- If direct local `curl` to the generated image URL returns `403`, that is expected; use the in-browser fetch/download path.
- If the remote browser is unavailable, only then consider the local/fallback browser path.

## When to inspect manually

Read `scripts/chatgpt_image_tailnet.py` when you need to:
- add aspect-ratio controls
- upload an input image before prompting
- send the final file directly over messaging
- adapt selectors if ChatGPT changes the UI
