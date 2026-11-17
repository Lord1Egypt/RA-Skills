## Description:

A股多Agent投研 guides agents in producing structured A-share investment research, debate-style analysis, limit-up/limit-down rule checks, and risk-oriented reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for A-share research workflows, including stock-data analysis, multi-agent debate summaries, portfolio or sentiment reports, and risk-control guidance. Investment-related outputs should be treated as informational and reviewed by a human before action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags mismatched SEO activation text that could confuse when the skill should be invoked.

Mitigation: Align the public description and activation guidance with the A-share research purpose before distribution.

Risk: The skill requests command execution without clear allowed-command boundaries.

Mitigation: Document exact permitted commands, credential handling, and user-confirmation requirements before enabling execution.

Risk: Investment research output could be mistaken for trading instructions.

Mitigation: Treat all investment output as informational and require separate human approval before trading or account changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/agent-research)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional JSON result examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include investment research summaries, API credential setup guidance, troubleshooting steps, and structured result metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
