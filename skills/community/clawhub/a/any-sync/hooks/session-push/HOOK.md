---
name: session-push
description: Auto-push workspace changes to GitHub on session end
metadata:
  openclaw:
    events: ["session_end"]
    requires:
      bins: [gh]
---

# Session Push Hook

Automatically pushes local workspace changes to the configured GitHub sync repo when a session ends. Only pushes if there are pending changes. Runs silently.
