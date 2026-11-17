## Description:

Automates collection and analysis of robotics competitor data from Google Search, map and social sources, and a local knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larthe](https://clawhub.ai/user/larthe)

### License/Terms of Use:

MIT-0

## Use Case:

Operators, market analysts, and developers use this skill to run a competitor scraper, inspect JSON and CSV outputs, and summarize competitor ratings, prices, locations, and source notes for robotics businesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unbundled local competitors_scraper.py script at a referenced workspace path.

Mitigation: Inspect and trust the local script before running the skill, and confirm the path points to the intended workspace file.

Risk: The artifact includes a hard-coded Telegram recipient for report delivery.

Mitigation: Replace the target with a recipient you control and confirm before sending any report externally.

Risk: The artifact suggests a sudo browser-install command for fuller scraping support.

Mitigation: Avoid the privileged install command unless an administrator has intentionally approved that host change.

## Reference(s):

- [Competitor Parser on ClawHub](https://clawhub.ai/larthe/skills/competitor-parser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON/CSV output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce competitors_data.json and competitors_data.csv when the referenced local scraper exists and runs successfully.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
