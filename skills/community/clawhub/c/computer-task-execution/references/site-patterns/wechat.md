---
kind: local-app
name: WeChat
app_id: com.tencent.xinWeChat
aliases: [微信, WeChat, xinWeChat]
updated: 2026-03-27
---

## Platform traits
- WeChat desktop messaging is treated as a local-app task.
- Reliable sending depends on correct window focus and visible thread verification.
- Success is preferred over silence for this target.

## Successful paths
- [2026-03-27] Verified send flow: `open -a WeChat` (fallback `open -a 微信`) → `Command+F` → paste contact name → `Enter` to open target chat → paste message → `Enter` to send.
- [2026-03-27] Connectivity test default: use the contact phrase `微信给小崽崽说 hi` and append a timestamp in the sent content for freshness checking.

## Preconditions
- The app is installed and launchable.
- Main window is available.
- Contact search accepts pasted text.
- The target contact can be uniquely selected from search.

## Verification
- Confirm in the visible target thread that the sent message appears after send.
- For test messages, verify the timestamp matches the current run.

## Unstable or failed paths
- [2026-03-27] Background-only keyboard flow is not the default because focus ownership cannot be reliably verified.
- [2026-03-27] Silent mode may be attempted only when explicitly requested, with lower confidence.

## Recommended default
- Use background preparation + short foreground execution + post-send verification.
- Prefer the verified local-app send chain above.

## Notes for future runs
- Default strategy is “prefer success,” even if short foreground focus is required.
