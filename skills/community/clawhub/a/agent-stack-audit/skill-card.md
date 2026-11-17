## Description:

Agent Stack Audit performs a recurring maintenance audit of automation stacks, identifying zombie scheduled tasks, dead scripts, unused API keys, superseded skills, stale memory files, and subscriptions that may need cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pingukim225](https://clawhub.ai/user/pingukim225)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to audit agent and automation stacks for unused, redundant, outdated, or healthy components and to prepare a ranked cleanup brief before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit may expose sensitive operational data such as scheduled jobs, API key inventory, account details, memory files, and subscription usage.

Mitigation: Before running the skill, define exact directories, scheduled jobs, accounts, and memory files in scope; prohibit reading or storing secret values; and require redaction in reports.

Risk: The skill allows limited code or cleanup changes after its audit, which could alter working automations if approval boundaries are unclear.

Mitigation: Run it in recommendation mode first and require explicit approval for every code, configuration, or cleanup change.

Risk: Tool and subscription recommendations can depend on current pricing, feature availability, and recent alternatives.

Mitigation: Require dated evidence for replacement recommendations and treat uncertain findings as needing user input rather than immediate cleanup.

## Reference(s):

- [ClawHub skill page: Agent Stack Audit](https://clawhub.ai/pingukim225/skills/agent-stack-audit)
- [ClawHub publisher profile: pingukim225](https://clawhub.ai/user/pingukim225)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with tables and optional cleanup notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports recommended actions before cleanup; cleanup changes require explicit user approval.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
