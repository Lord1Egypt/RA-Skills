---
kind: website
name: Outlook Web
domain: outlook.office.com
aliases: [Outlook, Outlook Web]
updated: 2026-03-27
---

## Platform traits
- Outlook Web is preferred for mailbox reading, triage, and many routine mailbox actions when browser login state exists.
- Browser state is easier to reread and verify than local desktop mail UI for most inspection tasks.

## Successful paths
- [2026-03-27] Mail-read flow: open Outlook Web → open target mailbox/folder → open the target message in-page → inspect content/state → confirm by rereading message/thread state.
- [2026-03-27] Triage flow: open Outlook Web → locate target message → perform action (flag/move/archive/etc.) → confirm the post-action message state in-page.
- [2026-03-27] Reply/draft flow: open target message in web UI → compose in-page → verify target thread and visible draft state before send/submit.

## Preconditions
- Browser login state is available.
- Mailbox content is reachable in Outlook Web.

## Verification
- Confirm by rereading message/thread/folder state in the web UI.
- Use visible page confirmation if direct state read-back is insufficient.

## Unstable or failed paths
- [2026-03-27] Local Outlook app automation is not preferred when the web client can complete the same task with clearer verification.

## Recommended default
- Use Outlook Web first.
- Fall back to desktop only for desktop-specific capability gaps.

## Notes for future runs
- Retrieval, review, and mailbox-state confirmation are usually cleaner in the web client.
