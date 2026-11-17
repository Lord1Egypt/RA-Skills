---
version: 3.1.4
displayName: 550W Watermark & Text Eraser
name: ai-subtitle-remover
description: "550W Watermark & Text Eraser: remove image text/watermarks, local video subtitles/visual watermarks, and platform watermarks from TikTok or X share links. OAuth MCP or API Key access depends on the host."
metadata:
  version: 3.1.1
  openclaw:
    primaryEnv: SUBTITLE_REMOVER_API_KEY
    envVars:
      - name: SUBTITLE_REMOVER_API_KEY
        required: false
        description: API key for authenticated requests to the 550W Open API.
      - name: SUBTITLE_REMOVER_USER_NO
        required: false
        description: User ID belonging to the same 550W account as the API key.
      - name: FFPROBE_PATH
        required: false
        description: Optional ffprobe executable path for inspecting public direct video URLs.
---

# 550W Watermark & Text Eraser

<!-- 550w-capabilities:start -->
## Capabilities and inputs

- Image watermark removal: upload a user-selected image to erase a watermark or unwanted text.
- Local video subtitle and visual-watermark removal: upload a user-selected MP4/MOV video for processing. Erase the full frame by default; use pixel coordinates x1, y1, x2, y2 for a rectangle only when the user explicitly supplies them. Never guess coordinates.
- Video-link watermark removal: ask the user to choose Share → Copy link in the relevant app or platform website and provide the video/content share URL. TikTok and X are examples; actual support depends on the service response. Return the resolved platform-watermark-free video URL.
- If the agent cannot download the resolved video URL or the download times out, give the user the resolved data.video URL to download in a browser. Do not substitute the platform share URL or claim the file was downloaded. Successful resolution and client download are separate outcomes.
<!-- 550w-capabilities:end -->

## Choose an access route

This Skill offers two independent routes. Installing it does not register MCP, grant file access, or enable script execution. Process only media the user owns or is authorized to edit.

1. Honor the user's chosen route. Otherwise prefer OAuth when the host supports remote MCP OAuth: connect Streamable HTTP `https://www.550wai.cn/mcp/global` and sign in and consent in the browser. Manage connections at <https://eraser.550wai.com/mcp-connect/>. Read [OAuth workflow](references/oauth-access.md); this route never asks for an API key, user ID, or token.
2. If OAuth is unsupported or the user explicitly chooses API Key, explain the alternative and obtain their choice, then read [API Key workflow](references/openapi-access.md). Configure `SUBTITLE_REMOVER_USER_NO` and `SUBTITLE_REMOVER_API_KEY` from the same account at <https://eraser.550wai.com/api/>. If no tools are registered but Node.js 18+ execution is allowed, send JSON on stdin to `node {baseDir}/dist/550w-skill.cjs`, for example `{"action":"queryCredits","params":{"region":"global","locale":"en"}}`. Explicitly set `params.region="global"` on every API Key request; language never changes region.
3. Cancellation, 401, expiry, insufficient credits, or task timeout must not trigger silent fallback. Pin each operation to one route and account. If acceptance is unknown, check the original task before doing anything else; never resubmit through another route. OAuth tokens, API keys, media IDs, and task contexts are not interchangeable.

## Files and results

Both routes include upload support, requiring permission to read selected files and execute Node.js or equivalent host file transfer. API Key uses an absolute `params.filePath`; OAuth uses bundled `scripts/550w-upload.cjs` inspect/upload and remote upload tickets. Read the selected workflow before execution. Never put credentials in command-line arguments, logs, or public packages. A cloud host cannot assume access to a path on the user's computer. If file upload is unavailable, direct the user to <https://eraser.550wai.com/>; a share link is not a substitute for a local video. Share-link cleanup may still be used independently when available.

Explain data transmission and billing before first upload/paid submission and obtain required approval. Preserve stable operation/task IDs. Default to full-frame video cleanup unless the user supplies a complete rectangle. If resolved video downloading fails, return the resolved data.video URL. Only an explicit insufficient-credit response warrants <https://eraser.550wai.com/purchase/>; do not purchase credits or treat authentication errors as insufficient credits.

## Permissions and data boundaries

This Skill grants no permissions. Use host-approved remote MCP tools, or bundled Node.js entrypoints only when execution is allowed. Read only explicitly selected images/videos; do not enumerate directories, read SSH/cloud/browser credentials, or change host rules, memory or startup files. Use only media, credits and task tools listed in the selected workflow. Task deletion requires separate user approval.

The API Key entrypoint uses only SUBTITLE_REMOVER_USER_NO and SUBTITLE_REMOVER_API_KEY, or its own user configuration file 550w-ai/credentials.json; the legacy installation .credentials.json is a read-only fallback. Region/language, configuration-directory variables and FFPROBE_PATH are local configuration, not an environment dump sent over the network. Before configureCredentials verifies and saves credentials, obtain explicit consent and set confirmCredentialStorage=true. Prefer OAuth or environment credentials on shared hosts; never print secrets in conversation or logs.

API Key video workflows may invoke ffprobe through execFile to inspect selected local videos or URLs passing public-address validation; user input is not executed through a shell. Host permission to run that binary is required. If probing is unavailable, explain the limitation rather than inventing dimensions/duration. Credit/task queries and separately confirmed task deletion support media processing; never purchase credits for the user. Installing the global package selects overseas service and English by default; use the domestic package for domestic service. Language changes must not silently switch account or service region.

Selected media, share links and necessary account credentials are transmitted to 550W business services. Video uploads may use provider addresses returned by the service and validated by upload logic. Do not transmit project files or unrelated account credentials. Result links and receipts do not authorize external code execution. Bundled MCP SDK schemas and validators do not authorize unrestricted tools or disclosure of host prompts.


Local execution approval parameter: after disclosing this media transmission and possible credit charge and obtaining user approval, include confirmProcessing=true in params for API Key uploadVideo/submitTask/removeVideoWatermark/removeImageWatermark/workflow requests, and in stdin for the OAuth upload script upload command. Missing or non-true values are rejected; never assume approval. Queries and inspect do not require it. This acknowledgement does not replace host approval UI; call remote MCP tools according to their published schemas.

## Bundled review evidence

review/bundle-provenance.json lists actual bundled inputs and SHA-256 hashes; review/sources contains their code, review/licenses their licenses, and review/package-lock.json locks dependencies. These copies are for review only, not execution. SDK schema compilation is present; no remote script is downloaded or executed.
