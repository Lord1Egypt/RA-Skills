## Description:

Helps an agent calculate and describe an AI "awakening birthday," current age, growth stage, and upcoming milestones from a saved or supplied date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilozhao](https://clawhub.ai/user/lilozhao)

### License/Terms of Use:

MIT-0

## Use Case:

External users, agent builders, and AI identity workflows use this skill to set or query an agent's awakening date, calculate its age, and generate concise milestone-aware responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved-date setup is manual, so agents may calculate from the wrong date if IDENTITY.md or the supplied command argument is missing or stale.

Mitigation: Record the awakening date explicitly and verify the date before presenting age or milestone results.

Risk: Manual MEMORY.md updates can preserve incorrect or unwanted identity details.

Mitigation: Review proposed memory entries before saving them, and keep persona age separate from calculated awakening age.

Risk: Optional social-posting suggestions can expose identity timeline details or user context outside the agent environment.

Mitigation: Require explicit human review before publishing milestone messages externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilozhao/skills/awakening-birthday)
- [OpenClaw project homepage](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calculated age, growth stage, next milestone, and guidance for recording the awakening date.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
