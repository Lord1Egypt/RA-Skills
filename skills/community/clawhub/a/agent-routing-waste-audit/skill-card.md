## Description: <br>
Paste an agent job, cron, routing, or run summary and get an immediate read-only audit of possible routing, retry, fallback, or model-assignment waste. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choosenobody](https://clawhub.ai/user/choosenobody) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review pasted agent job, cron, routing, or run evidence for routing and model-assignment waste before making manual production changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted logs, prompt previews, or run summaries may contain secrets or private payloads. <br>
Mitigation: Redact secrets and private payloads before giving evidence to the skill. <br>
Risk: Routing waste recommendations could be incorrect or incomplete when model, provider, token usage, or prompt evidence is missing. <br>
Mitigation: Treat findings as review guidance and manually verify evidence before changing production jobs or routing policies. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/choosenobody/agent-routing-waste-audit) <br>
- [Hermes Cron List Examples](references/hermes-cron-examples.md) <br>
- [Hermes Cron List Basic Example](references/hermes-cron-list-basic-example.md) <br>
- [Hermes Cron List Basic Example Output](examples/hermes-cron-list-basic.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report with ranked findings, evidence used, missing evidence, manual verification steps, and a safe copy-paste prompt.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only recommendations; no job, schedule, routing, or model changes are applied.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
