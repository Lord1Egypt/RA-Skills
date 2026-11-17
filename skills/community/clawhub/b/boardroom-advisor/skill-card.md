## Description:

Consult a virtual board of 4 strategic advisors (Donald Miller, Seth Godin, Alex Hormozi, Daniel Priestley) on any major business decision through two rounds of argument and rebuttal, followed by a decision brief, interactive dashboard, and clear recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[batsirai](https://clawhub.ai/user/batsirai)

### License/Terms of Use:


## Use Case:

Business operators, founders, and teams use this skill to deliberate major strategic decisions through four advisor personas, structured debate, rebuttal, and a final recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate proactively for major business decisions and may gather sensitive business context.

Mitigation: Narrow activation to explicit phrases such as 'consult the board' or require confirmation before gathering context.

Risk: The workflow may send confidential business context to OpenRouter when an API key is configured.

Mitigation: Avoid providing confidential financial, customer, or strategy information unless the user accepts the external model provider's data handling.

Risk: The skill writes decision briefs, dashboards, and print-ready files into the working directory.

Mitigation: Confirm the output location and review generated files before relying on or sharing them.

## Reference(s):

- [Boardroom model: OpenRouter + Claude Opus 4.6](references/openrouter-board-model.md)
- [OpenRouter Claude Opus 4.6 model page](https://openrouter.ai/anthropic/claude-opus-4.6)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, self-contained HTML, configuration snippets, and conversational synthesis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a decision folder containing a decision brief, interactive dashboard, and optional print-ready HTML.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
