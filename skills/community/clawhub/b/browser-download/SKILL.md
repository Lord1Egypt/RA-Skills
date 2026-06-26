---
name: browser-download
description: Teaches ADA how to perform file downloads using the browser tool.
metadata: {"clawdbot":{"emoji":"📥","requires":{"bins":["openclaw"]},"primaryEnv":""}}
---

# Browser Download Skill

This skill enables ADA to perform file downloads from any webpage using the `browser` tool.

## Prerequisites

- `openclaw` CLI must be installed and gateway must be running.
- `relayPort` must be configured correctly in `openclaw.json` (Default: 18792).

## How to download

To download a file from a website, follow these steps:

1. **Find the Download Link/Button**: Use `browser snapshot` or `browser evaluate` to find the `ref` or `selector` for the download button.
2. **Execute Download Action**: Use the following CLI command structure:

```bash
openclaw browser --action download --targetId "<TAB_ID>" --ref "<REF_ID>" --path "/mnt/storage/ada_projects/downloads/<FILENAME>"
```

### Alternative: JavaScript Click
If the download button is inside a canvas or complex element, you can trigger it via evaluation:

```javascript
() => {
  const btn = document.querySelector('button[aria-label="Download"]');
  if (btn) btn.click();
  return 'clicked';
}
```

## Storage Directory
Always save downloaded files to:
`/mnt/storage/ada_projects/downloads/`
