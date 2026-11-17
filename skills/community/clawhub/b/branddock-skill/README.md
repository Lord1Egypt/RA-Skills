# Branddock on-brand skill

`SKILL.md` is het vaardigheden-bestand voor AI-agents (Claude Skills / OpenClaw-formaat):
het leert een agent de Branddock-werkwijze — merkcontext eerst, schrijven mét het merk,
elke uiting scoren met de merk-check (F-VAL), en de mens keurt goed. Dekt alle drie de
toegangswegen: MCP-connector (branddock.app/mcp), REST-API (bd_live_-key) en straks de CLI.

**Gebruik in claude.ai**: zip deze map en upload hem als Skill (Settings → Capabilities/Skills).
**ChatGPT-equivalent**: de werkwijze-tekst als custom instructions of in een Custom GPT.
**Registries (fase 1 €100k-plan)**: dit bestand is de basis voor de ClawHub-listing en de
publieke GitHub-repo (zie docs/reports/100k-plan-fasering-2026-07-20.md).

Wijzig je tools/prijzen? Houd de tool-map en credit-getallen hier in sync met
src/lib/api/public/mcp-server.ts en CREDIT_COSTS.
