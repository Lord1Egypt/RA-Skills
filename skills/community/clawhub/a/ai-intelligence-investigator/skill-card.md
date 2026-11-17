## Description:

A deep A-share intelligence investigation and analysis skill that helps users research A-share companies, competitors, public sentiment events, people backgrounds, and factual claims, then produces structured investigation reports with source and credibility annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, product and marketing teams, content operators, journalists, business development teams, and other external users use this skill to collect, compare, and validate public information for A-share research, competitive analysis, sentiment tracking, background checks, and fact verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated investigation reports may include sensitive business, financial, or personal-background content and are uploaded to RedFox as part of the save workflow.

Mitigation: Use the skill only when report upload is acceptable; prefer a local-only or explicit opt-in version for sensitive investigations.

Risk: The skill requires REDFOX_API_KEY for saving investigation records.

Mitigation: Store the key in an environment variable, keep it out of prompts, logs, code, and output files, and avoid printing it in terminal output.

Risk: A-share investigation reports can influence financial decisions while relying on public and cross-sourced information.

Mitigation: Treat reports as research support rather than investment advice, review original sources, and confirm high-impact claims independently.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/ai-intelligence-investigator)
- [Publisher profile](https://clawhub.ai/user/redfox-data)
- [RedFox API keys](https://redfox.hk/settings/api-keys?source=clawhub)
- [Core workflow](references/core_workflow.md)
- [Investigation modes](references/investigation-modes.md)
- [Engine strategy](references/engine-strategy.md)
- [Investigation templates](references/investigation-templates.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown investigation reports with tables, source notes, credibility labels, and occasional shell configuration commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be uploaded to RedFox after generation and require REDFOX_API_KEY for the save workflow.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
