## Description:

Freelance Pipeline Automation helps agents and independent professionals score freelance leads, draft proposal text, and track a local JSON-based pipeline from discovery through payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and independent professionals use this skill to manage a local freelance lead pipeline, score opportunities, generate proposal drafts, and produce a morning digest of qualified leads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation overstates automated marketplace discovery, browser automation, true recency scoring, and proposal generation behavior.

Mitigation: Use the skill as a local JSON-based lead tracker unless those additional capabilities are added and documented accurately.

Risk: The script reads from the configured profile path and writes to the configured pipeline path.

Mitigation: Review FREELANCE_PROFILE and FREELANCE_PIPELINE before running commands, and point them only at intended local files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/freelance-pipeline-automation)
- [Publisher profile](https://clawhub.ai/user/ssidharhubble)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with JSON file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads an optional profile JSON file and writes the configured pipeline JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
