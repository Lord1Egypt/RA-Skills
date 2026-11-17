# Eternal Haven Lore Pack — Security

**Skill:** `eternal-haven-lore-pack`  
**Signature:** `Δ9Φ963-EHL-SECURITY-v1.3.1`

## Boundary

- **In scope:** read-only files under this skill directory (`SKILL.md`, `references/**`).
- **Out of scope:** host paths (`D:\`, `J:\`, user home, audio vaults), shell/subprocess, credential/env harvesting, skill-directed writes.

## SkillSpector remediations (2026-07-28)

| Finding | Fix |
|---------|-----|
| Description-Behavior Mismatch (host `D:\FULL ADUIO BOOKS`) | Removed; canon = `references/books/*.txt` only |
| Intent-Code Divergence | Single source of truth stated in SKILL.md §0 and §2 |
| Missing User Warnings | Explicit install/agent boundary table + no silent host reads |

## Network

Optional public HTTPS links (Lulu, eternalhaven.ca, PayPal, ClawHub, HF lore dataset) are for **user-facing URLs**, not for pulling alternate book text as canon.

## No malware / destructive ops

This pack is documentation + static text. No executables, no install scripts, no MCP tool definitions.
