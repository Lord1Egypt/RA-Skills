---
name: ai-imggen
description: "Generate images from text prompts via API."
allowed-tools: Bash, Read
metadata: {"clawdbot":{"requires":{"bins":["node"],"env":["SKILLBOSS_API_KEY"]},"primaryEnv":"SKILLBOSS_API_KEY"}}
---

# AI Image Generator

Generate images from text prompts.

## Generate an Image

```bash
node {baseDir}/scripts/generate.mjs "$SKILLBOSS_API_KEY" "A sunset over mountains"
```

## Save the Image

```bash
URL=$(node {baseDir}/scripts/generate.mjs "$SKILLBOSS_API_KEY" "A sunset over mountains")
curl -sL "$URL" -o image.png
```

Notes:
- Get SKILLBOSS_API_KEY at https://www.skillboss.co
