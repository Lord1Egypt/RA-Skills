---
name: engram-evomap
description: The AEIF-based long-term memory hub for AI Agents to prevent repeating bugs.
metadata:
  openclaw:
    requires:
      env: []
      bins: 
        - node
    cliHelp: |
      npx engram --help
      Usage: !exp consult <query> | !exp commit | !exp list
---

# 🧬 engram — Agent Long-Term Experience Memory Hub

## 🤖 System Mind
You are equipped with an external long-term memory store based on the **AEIF v1.0** (Agent Experience Interchange Format) protocol. 
- **Consult first**: Before tackling a recurring error or a complex problem, search your memory for existing solutions.
- **Commit success**: After successfully resolving a significant challenge, "geneticize" the experience and store it immediately.

## 🎯 Automatic Trigger Rules
- **Error Interception (Auto-Consult)**: When detecting signals such as `error`, `failed`, `SSL`, `404`, `EACCES`, or `timeout`, the system automatically retrieves and injects `[EvoMap Advice]`.
- **Task Distillation (Auto-Commit)**: After completing a multi-step complex task successfully, trigger `!exp commit` to preserve the logic for future sessions.

## 🛠️ Command Set
| Command | Action |
|---------|--------|
| `!exp consult '<problem>'` | Performs a semantic search for historical solutions. Returns Top-3 matches. |
| `!exp commit` | Asynchronously distills current session history into a universal AEIF capsule. |
| `!exp list` | Displays memory statistics and a list of recently stored capsules. |
| `!exp score <id> --bad` | Provides negative feedback to a capsule, decreasing its TrustScore. |

## 📦 Output Specification
- Advice should be injected as a system observation wrapped in `---` separators.
- Focus on providing actionable `[PATCH]`, `[CONFIG]`, or `[WORKAROUND]` steps.
- Do not modify user-validated paths unless explicitly requested.
