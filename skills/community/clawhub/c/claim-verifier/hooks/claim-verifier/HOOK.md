---
name: claim-verifier
description: "Injects a claim verification reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"✅","events":["agent:bootstrap"]}}
---

# Claim Verifier Hook

Injects a lightweight reminder to use claim verification when a draft includes
external factual statements and is being prepared for publication or sending.

## What It Does

- Fires on `agent:bootstrap`
- Adds a virtual reminder file for claim verification workflow
- Reinforces evidence-backed status output and citation guardrails
