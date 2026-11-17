## Description:

Agent Chronicle generates reflective markdown diary entries for agents, with optional quote, curiosity, decision, relationship, mood-analysis, weekly-digest, resurfacing, and scheduled auto-generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to turn OpenClaw session context into reflective diary entries, weekly digests, and diary analytics for agent memory and self-review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local session-derived memory and can create long-lived diary, quote, decision, mood, and relationship records.

Mitigation: Use it only in a low-sensitivity workspace, keep optional memory integration and relationship tracking disabled unless explicitly needed, and review entries before saving or sharing them.

Risk: Scheduled auto-generation depends on command execution approvals.

Mitigation: Avoid blanket automation approvals; approve only the exact commands and working directories required for the diary job.

Risk: Exporting diary markdown to PDF or HTML can preserve or expose sensitive generated content.

Mitigation: Review diary content before export and avoid exporting untrusted diary markdown until renderer resource fetching is constrained.

## Reference(s):

- [Agent Chronicle ClawHub listing](https://clawhub.ai/robbyczgw-cla/skills/agent-chronicle)
- [OpenClaw automations documentation](https://docs.openclaw.ai/automation/cron-jobs)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown diary entries and reports, optional JSON analysis, shell command examples, configuration JSON, and optional HTML/PDF exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated diary entries target about 400-600 words when using the default configuration.]

## Skill Version(s):

0.8.0 (source: frontmatter, skill.json, changelog, released 2026-08-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
