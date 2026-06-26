# 🔒 Privacy & Data Governance — Claude Code Assist

> **Last updated:** 2026-06-18
> **Applies to:** v1.0.1+

---

## 1. What This Skill Does

Claude Code Assist is a setup and configuration tool:

| Action | Scope |
|--------|-------|
| Environment check | Reads Node.js/Git/npm versions installed on your machine |
| API configuration | Writes provider settings to Claude Code's config file |
| Verification | Tests connectivity to configured provider |

---

## 2. What This Skill NEVER Does

- ❌ Send your API keys to third-party servers
- ❌ Read or transmit your code or documents
- ❌ Exfiltrate system information
- ❌ Modify files outside of Claude Code's config directory
