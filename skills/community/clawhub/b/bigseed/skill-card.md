## Description:

Big Seed is an AI diary and memoir skill that records short journal entries, builds a personal portrait from those records, and generates stories, scripts, reports, summaries, and memory prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobenfang](https://clawhub.ai/user/kobenfang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Big Seed to capture diary-like thoughts, memories, images, and life events, then ask an agent to summarize patterns, build a personal portrait, and create memoir-style stories or weekly journal reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes diary-like personal data in the bundled artifact.

Mitigation: Clean bundled journal records before release or installation, and review stored memory files before handling private user memories.

Risk: Weekly chat summaries can disclose sensitive facts inferred from journal records even when raw records remain local.

Mitigation: Make recurring summaries explicit and easy to disable, and treat generated summaries as sensitive personal information.

Risk: Delete and disable controls are described but not well supported by the bundled script behavior.

Mitigation: Add tested delete and subscription-disable controls before using the skill with private memories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kobenfang/skills/bigseed)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON-backed journal records and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate recurring weekly summaries, profile summaries, stories, scripts, reports, and statistics from local journal records.]

## Skill Version(s):

2.0.16 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
