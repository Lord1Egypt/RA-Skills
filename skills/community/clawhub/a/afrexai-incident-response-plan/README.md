# Incident Response Plan Generator

**By AfrexAI** | [clawhub.com](https://clawhub.com)

Generate tailored incident response plans for AI agent deployments and SaaS operations. Covers detection through post-mortem.

## What It Does

Builds a complete incident response playbook:

- **Detection & Alerting** — What triggers an incident, who gets paged
- **Triage & Classification** — Severity levels, impact assessment
- **Containment** — Isolate the blast radius, preserve evidence
- **Recovery** — Restore service, verify integrity
- **Post-Mortem** — Root cause, timeline, action items, blameless culture

## Output

- Severity classification matrix
- Role-based response procedures
- Communication templates (internal + customer-facing)
- Escalation paths with SLA targets
- Post-mortem template with 5-whys
- Runbook for common AI agent failure modes

## Usage

```
Generate an incident response plan for:
Service: AI-powered customer support agents
Scale: 500 conversations/day, 3 AI agents
Stack: OpenAI API, PostgreSQL, AWS ECS
SLA: 99.9% uptime, 30s response time
Team: 4 engineers, 1 ops lead
Compliance: SOC2, GDPR
```

## Works With

Part of the **Enterprise AI Deployment Pipeline**:

1. **[AI Adoption Readiness](https://clawhub.com/skills/afrexai-ai-adoption-readiness)** → Are you ready for AI?
2. **[Compliance Readiness](https://clawhub.com/skills/afrexai-compliance-readiness)** → Are you regulatory-ready?
3. **[Change Management Plan](https://clawhub.com/skills/afrexai-change-management-plan)** → How do you roll it out?
4. **[Vendor Risk Assessment](https://clawhub.com/skills/afrexai-vendor-risk-assessment)** → Which AI vendor to pick?
5. **Incident Response Plan** (this) → What if it breaks?
6. **[SLA Monitor](https://clawhub.com/skills/afrexai-sla-monitor)** → How do you keep it running?

## Install

```bash
clawhub install afrexai-incident-response-plan
```

---

Built by [AfrexAI](https://afrexai.com) — managed AI agents for businesses that want results, not science projects.
