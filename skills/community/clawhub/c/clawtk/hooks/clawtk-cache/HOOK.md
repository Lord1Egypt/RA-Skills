---
name: clawtk-cache
description: Semantic task caching for ClawTK Pro — skips redundant tool calls by returning cached results
event:
  - before_tool_call
  - tool_result_persist
priority: 50
---

Caches tool call results in a local SQLite database. When a semantically
identical tool call is detected, returns the cached result instead of
re-executing. Most effective for repeated file reads, test runs, and
project structure queries. Pro feature only.
