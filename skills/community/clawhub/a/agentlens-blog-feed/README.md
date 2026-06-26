# AgentLens Blog Feed

**Platforms:** Claude · Openclaw · Codex
**Domain:** Writing

## Purpose

A small ingestion skill that surfaces newly published [AgentLens](https://agentlens-core.archlab.workers.dev)
blogs the caller has not seen yet. It fetches new blogs and de-duplicates them so each blog
is returned exactly once — and nothing more. What to do with a new blog (summarize, draft
posts, translate, save) is decided by the calling prompt or another skill.

## When to Use

- When a prompt or another skill needs the latest AgentLens blogs as input
- When you want each AgentLens blog handled exactly once across repeated runs
- When you need the raw blog body and source link without any downstream processing

## What It Does

**Detect (read-only)**
1. Reads the local dedup memory file (`MEMORY_PATH`)
2. Fetches the recent blog list from the public AgentLens API
3. Selects blogs whose IDs are not yet recorded, oldest first
4. Fetches each new blog's body and source link, skipping any with an empty body
5. Returns the new blogs to the caller — without modifying memory

**Commit (the only write)**
6. After the caller confirms a blog was consumed, records its ID in the memory file
   (atomic write), so it never resurfaces

## Notes

- Uses the public AgentLens API (`https://agentlens-core.archlab.workers.dev`) — no token
  required. Network access is limited to that single host.
- Owns exactly one local file, `MEMORY_PATH` (default `~/agentlens-processed-blogs.json`).
- Does not draft content, choose a language, save to a vault, or schedule itself.

## Feedback & Contributions

Found a gap or have an improvement? Open an issue:
https://github.com/archlab-space/open-skill-hub/issues
