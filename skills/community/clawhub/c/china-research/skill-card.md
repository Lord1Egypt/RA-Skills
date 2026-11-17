## Description:

China Research helps agents research Chinese social media discussions for a user-provided topic and generate a cited market-research report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyunfeng8](https://clawhub.ai/user/wuyunfeng8)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product teams, and market researchers use this skill to inspect Chinese platform discussions, identify user pain points, compare existing solutions, and summarize market opportunities with cited sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented command examples place user-provided topics directly into shell commands, which can create command-injection risk if followed literally.

Mitigation: Review search topics before execution and rewrite examples to use structured tool calls or shell-safe argument passing.

Risk: The skill is intended for web and social-platform research, so confidential or sensitive research topics could be exposed to external search services.

Mitigation: Use the skill only with non-confidential research topics, as recommended by the security evidence.

## Reference(s):

- [Domestic social media platform search strategy](references/platforms.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research report with cited source list and search-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are organized around core findings, user pain points, existing solutions, market opportunities, and references.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
