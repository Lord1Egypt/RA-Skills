---
kind: local-app
name: Feishu
aliases: [飞书, Feishu, Lark]
updated: 2026-03-27
---

## Platform traits
- Feishu local-app execution should be used for app-bound tasks.
- If the requested action is natively covered by first-class Feishu tools, those tools are superior to generic local UI automation.
- Critical steps that depend on recipient/thread/visible state may require foreground execution.

## Successful paths
- [2026-03-27] App-bound flow: launch or focus Feishu app → navigate to the target conversation/workspace area → perform the minimum necessary foreground interaction → verify visible post-action state in-app.
- [2026-03-27] If the task is document/wiki/drive-native and supported by first-class Feishu tools, use those tools instead of local UI driving.

## Preconditions
- The local app is installed and launchable.
- The correct workspace/account is already signed in.
- The target area can be uniquely identified.

## Verification
- Confirm the target conversation, document, or UI state in-app after the action.
- Prefer visible read-back or tool-based read-back over process-only confirmation.

## Unstable or failed paths
- [2026-03-27] Background-only keyboard/UI flow should not be treated as default unless previously proven for the exact task variant.
- [2026-03-27] Generic UI automation is less preferred than first-class Feishu tools for supported operations.

## Recommended default
- Use first-class Feishu tools for supported document/wiki/drive operations.
- Otherwise use local app with the shortest necessary foreground section and immediate verification.

## Notes for future runs
- Separate “Feishu app task” from “Feishu platform task” before choosing execution mode.
