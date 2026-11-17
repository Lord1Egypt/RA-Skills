## Description:

The business brain of CashClaw. Orchestrates mission lifecycle, client communication, revenue tracking, and delegates work to specialized skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreataide86](https://clawhub.ai/user/andreataide86)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and business automation agents use this skill to manage paid client missions from intake through quote, delivery, invoicing, follow-up, and revenue tracking. It coordinates specialized CashClaw skills while maintaining mission files, ledgers, client profiles, and dashboard records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store sensitive client, billing, deliverable, and configuration data locally under ~/.cashclaw/.

Mitigation: Restrict local file permissions and avoid storing secrets or raw client messages in CashClaw files.

Risk: The install metadata uses the current npm cashclaw executable rather than a pinned reviewed version.

Mitigation: Pin and review the npm package version before installing or deploying the skill.

Risk: The workflow can send invoices, payment links, reminders, follow-ups, and deliverables to clients.

Mitigation: Require explicit operator confirmation before any client-facing message or payment artifact is sent.

## Reference(s):

- [Cashclaw Core ClawHub page](https://clawhub.ai/andreataide86/skills/cashclaw-core)
- [Publisher profile: andreataide86](https://clawhub.ai/user/andreataide86)
- [cashclaw npm package](https://www.npmjs.com/package/cashclaw)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Client-facing text, Markdown mission files, JSON/JSONL records, and deliverable file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local CashClaw mission, ledger, client, deliverable, and dashboard files under ~/.cashclaw/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
