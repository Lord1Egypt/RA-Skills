---
name: factucat-cli
description: Use this skill when an agent needs to install, update, authenticate, or operate the FactuCat CLI to create Mexican CFDI 4.0 invoice drafts, assign customers or receiver data, add concepts, preview invoices, stamp them, send them through customer contact channels, or download XML/PDF artifacts on factucat.com.
metadata: {"openclaw":{"emoji":"🧾","homepage":"https://github.com/factucat/ai-skills/tree/main/factucat-cli","skillKey":"factucat-cli","primaryEnv":"FACTUCAT_API_KEY","requires":{"bins":["factucat"]},"install":[{"id":"npm","kind":"node","package":"@factucat/cli","bins":["factucat"],"label":"Install FactuCat CLI (npm)"}]}}
---

# FactuCat CLI

FactuCat CLI operates FactuCat Cloud from the command line. It is specifically for **Mexican CFDI 4.0 invoicing**, not for generic invoicing or self-hosted deployments.

## Use This Skill When

- A user wants to install or update the FactuCat CLI
- A user needs to authenticate with a FactuCat API key
- An agent needs to create, edit, preview, or stamp CFDI drafts from the terminal
- A workflow needs unattended CLI execution with `--json` and `--no-input`
- A user wants to download XML or PDF artifacts for a stamped invoice

## Operating Rules

- Treat `https://factucat.com` as the production service endpoint
- Use Mexican CFDI and SAT terminology in explanations and examples
- Prefer interactive flows for humans in a TTY
- Prefer `--json` and `--no-input` for agents, scripts, and deterministic automation
- Use `factucat invoice show` for the full preview before timbrado
- When a task involves fiscal vocabulary or CFDI semantics, read [references/mexico-cfdi-context.md](references/mexico-cfdi-context.md)

## Workflow Guide

1. For installation, updates, and authentication, read [references/install-and-auth.md](references/install-and-auth.md)
2. For a human-operated invoice flow, read [references/interactive-flows.md](references/interactive-flows.md)
3. For agent or script execution, read [references/unattended-flows.md](references/unattended-flows.md)
4. If anything fails, read [references/troubleshooting.md](references/troubleshooting.md)

## Practical Notes

- `factucat invoice create --customer "..."` is a shortcut that creates a draft and tries to resolve a customer by name or RFC
- `factucat invoice add-item` can infer SAT product code, SAT unit code, IVA, and retained ISR if omitted
- `factucat invoice set-meta --currency USD` can infer the official DOF exchange rate if `--exchange-rate` is omitted
- `factucat invoice stamp` can be interactive and ask about sending the stamped invoice through registered customer contact channels
- For issued invoices, commands that accept an invoice reference can usually take either a UUID or folio
