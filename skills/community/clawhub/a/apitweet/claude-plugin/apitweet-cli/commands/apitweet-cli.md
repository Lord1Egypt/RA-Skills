---
description: Use the apitweet skill to install, configure, test, or run apitweet CLI workflows.
---

# apitweet CLI

Use the installed `apitweet-cli` skill for this task.

Prefer this command when the user wants to:

- install or run the `apitweet` CLI
- configure API keys, app profiles, or auth profiles
- inspect request construction with `--dry-run`
- call apitweet endpoints with convenience commands or raw paths
- fetch global trending tweets with `trending tweets`
- publish Markdown files as X articles with `article publish-md`

Default behavior:

1. Check whether `apitweet` is available.
2. Use saved app auth or `APITWEET_KEY` for read requests.
3. Require a saved profile or explicit cookie for write requests.
4. Prefer convenience commands first.
5. Use `--dry-run` before real write actions unless the user clearly asks to execute them.
