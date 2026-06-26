---
kind: website
name: Feishu Web
domain: my.feishu.cn
aliases: [Feishu Web, Lark Web, 飞书网页]
updated: 2026-03-27
---

## Platform traits
- Feishu web is preferred for web-native Feishu tasks when browser state is available.
- For wiki/doc navigation, browser flow or first-class Feishu tools are preferred over generic local-app UI exploration.

## Successful paths
- [2026-03-27] Web-navigation flow: open target Feishu page in browser → inspect or operate in-page → reread page/object state after the action.
- [2026-03-27] For wiki/doc access, prefer browser or first-class Feishu tools before considering local-app UI control.

## Preconditions
- Browser login state is available.
- The target content is reachable in Feishu web.

## Verification
- Confirm by rereading page state or verifying the target object in the web UI.
- Prefer first-class Feishu tools when available for the task type.

## Unstable or failed paths
- [2026-03-27] Generic local-app UI automation is less preferred when the same result is available by browser flow or first-class tool.

## Recommended default
- Use browser or first-class Feishu tools first for web-native tasks.
- Use local app only when the task is specifically app-bound or browser flow is unsuitable.

## Notes for future runs
- If the task can be satisfied through Feishu tool APIs, that should usually beat browser driving.
