---
kind: website
name: Microsoft Teams
domain: teams.microsoft.com
aliases: [Teams, Microsoft Teams]
updated: 2026-03-27
---

## Platform traits
- Teams web is preferred when browser login state is present and the task is available in the web UI.
- Browser execution is easier to verify than local-app UI for chat/calendar/file reading and many routine actions.

## Successful paths
- [2026-03-27] Calendar/read flow: open Teams web in browser → navigate to Calendar view → inspect visible events and details in-page → confirm by rereading event state in the page.
- [2026-03-27] Chat/read flow: open Teams web → open target chat/channel in web UI → inspect visible thread state → confirm by rereading the thread after any action.
- [2026-03-27] If composing or replying in web UI, prefer in-page recipient/thread confirmation before submission.

## Preconditions
- Browser login state is available.
- The relevant workspace/account is already accessible in browser.
- The requested task is supported in Teams web.

## Verification
- Prefer DOM/state read-back in browser after the action.
- Use visible page confirmation only when direct reread is not enough.

## Unstable or failed paths
- [2026-03-27] Local-app UI automation is not the default when the same task is available in the web client with better state visibility.
- [2026-03-27] Do not default to keyboard-only local-app navigation when browser verification is available.

## Recommended default
- Use Teams web first.
- Fall back to local app only when the web client lacks the capability or is specifically unsuitable for the task.

## Notes for future runs
- For calendar and chat inspection, browser flow should usually win on verification quality.
