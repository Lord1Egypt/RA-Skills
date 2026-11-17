## Description:

Evidence Collector guides agents through screenshot-based QA review and reality checking of implemented web interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouqkt](https://clawhub.ai/user/zhouqkt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA reviewers use this skill to produce evidence-based visual QA reports, compare implementations against specifications, and document interaction or responsive issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intentionally skeptical and may bias QA reports toward finding failures even when zero issues are justified.

Mitigation: Review each finding against the cited visual evidence and permit zero findings when the evidence supports that conclusion.

Risk: The skill encourages persistent memory about developer behavior beyond simple evidence collection.

Mitigation: Disable or limit retention of developer-specific observations unless that retention is explicitly desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouqkt/skills/agency-evidence-collector)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with evidence references and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference screenshots and test-results JSON produced by the user's QA workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
