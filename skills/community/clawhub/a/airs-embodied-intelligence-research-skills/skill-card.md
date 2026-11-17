## Description:

AIRS招投标订单采集与核查 helps agents run a reusable robotics industry research workflow for entity confirmation, Tianyancha bidding evidence collection, third-party order verification, LLM-assisted case extraction, standardized ingestion tables, and case quality review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airs-guest](https://clawhub.ai/user/airs-guest)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research analysts use this skill to collect public bidding evidence, verify robotics orders, extract embodied-intelligence deployment cases, and prepare reviewed case-library ingestion outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses a logged-in browser session and Chrome remote debugging for Tianyancha access.

Mitigation: Run it only in a controlled local environment, use a dedicated Chrome profile, and close the remote-debugging browser session after collection.

Risk: Research records may be sent to a configurable OpenAI-compatible LLM provider.

Mitigation: Process confidential customer, internal, or regulated spreadsheets only with an approved provider and data-handling process.

Risk: Spreadsheet inputs and generated CSV outputs can carry dependency and formula-injection risk when opened in office tools.

Mitigation: Update or replace vulnerable spreadsheet/browser dependencies and neutralize CSV formula cells before opening generated files in Excel or similar tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/airs-guest/skills/airs-embodied-intelligence-research-skills)
- [Source homepage from ClawHub metadata](https://github.com/airs-guest/airs-embodied-intelligence-research-skills)
- [Tianyancha](https://www.tianyancha.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and CSV/Markdown file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local research data files under data/ when executed; those generated files are not part of the release package.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
