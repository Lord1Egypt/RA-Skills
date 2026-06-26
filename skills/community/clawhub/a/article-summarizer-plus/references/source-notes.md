# Source Notes

Use these heuristics only as guidance. Do not hardcode them as absolute rules.

## X / Twitter

- Single posts often render well in an interactive browser fallback even when fetch tools fail.
- X Articles can expose long-form content directly in the browser fallback.
- Comments / replies usually require browser scrolling.

## YouTube

- Fetch tools often fail or return poor results.
- The browser fallback can capture title, description, visible metadata, and visible top comments.
- If no transcript is available, be explicit that the “video content” summary may rely on title, description, and comment evidence rather than full spoken transcript.

## WeChat Articles

- Fetch may fail or be blocked.
- The browser fallback can sometimes pass simple access prompts.
- If a verification page appears, try low-risk entry actions first.

## Weibo

- Public profile shells may render, but detailed content often requires login.
- Distinguish clearly between visible profile metadata and inaccessible post stream content.

## Xiaohongshu / Other Social Pages

- Often require the browser fallback because of overlays, short links, or dynamic rendering.
- Try dismissing visible overlays before concluding the content is inaccessible.

## General Rule

Do not decide solely by platform name. Start with light retrieval by default, but escalate quickly when the visible evidence shows fetch is not enough.
