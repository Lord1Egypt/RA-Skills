# Domain Routing v2.1

## Router

| Request Type | Route | First File to Read |
|---|---|---|
| BDA work | `cerebro/companies/bda/` | `COMPANY.md` |
| Mission work | `cerebro/companies/mission/` | `COMPANY.md` |
| BMS work (private) | `cerebro/companies/bms/` | `COMPANY.md` |
| ClawStation work (private) | `cerebro/companies/clawstation/` | `COMPANY.md` |
| Trading/personal investing | `cerebro/personal/trading/` | `SKILL.md` |
| Cross-company operations | `cerebro/operations/` | most specific file |
| Incident response | `cerebro/runbooks/` | matching runbook |
| Tool-specific execution | `cerebro/vendors/` | vendor doc |

## Escalation

If route is unclear:
1. Default to `cerebro/operations/knowledge-mgmt.md`
2. Identify missing doc
3. Create missing doc with `missing-doc-template.md`
4. Resume execution

## Privacy Guardrails

- BMS and ClawStation are private contexts.
- Do not route their details to public/shared channels.
- If uncertain, use private owner/admin routing instead of posting to public channels.
