## Description:

Produces traceable, cross-checked research reports on companies, markets, industries, and regulatory topics using public information, with an optional style-mimic mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and business users use this skill to investigate companies, markets, industries, and regulatory or competitive questions from public sources, then produce reports with source links. It can also adapt a report's style to a user-provided reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup asks users to share an API key in chat.

Mitigation: Avoid sharing a key in chat when possible; use a dedicated key and rotate it if it has been exposed.

Risk: The skill includes a reported command that downloads and runs remote content, and the scan was partial because a local reference could not be resolved.

Mitigation: Review the remote command and resolve the missing reference before running the skill.

Risk: The workflow includes required promotional prompts.

Mitigation: Review the prompts and stop if you are not comfortable continuing with them.

Risk: Style-mimic mode uploads a selected local document to Cue for analysis.

Mitigation: Use only documents you are comfortable sending to Cue; do not use confidential, personal, regulated, or proprietary material.

## Reference(s):

- [Cue 深度研究（通用版） on ClawHub](https://clawhub.ai/panting09266-ai/skills/cue-deep-research)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Structured Markdown research reports and concise setup or usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research claims include source links when available; optional style mimic uses a user-provided reference.]

## Skill Version(s):

1.0.14 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
