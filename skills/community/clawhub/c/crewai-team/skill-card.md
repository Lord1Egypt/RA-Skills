## Description:

Uses a CrewAI multi-agent team to analyze product requirements and generate PRD documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[namechenxinyu](https://clawhub.ai/user/namechenxinyu)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, developers, and teams use this skill to turn a product idea into a PRD with market research, product design, technical architecture, implementation guidance, and QA planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable code includes a bundled API credential.

Mitigation: Remove the credential, rotate it before use, and require users to provide their own secret through environment configuration.

Risk: Install guidance includes curl-to-shell behavior and dependency installation that may not be pinned or locked.

Mitigation: Use reviewed installation steps with pinned or locked dependencies and avoid piping remote install scripts directly to a shell.

Risk: Product ideas and generated analysis may be sent to DashScope-compatible model calls or web search.

Mitigation: Review inputs for confidential information and confirm external data handling is acceptable before running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/namechenxinyu/skills/crewai-team)
- [DashScope Console](https://dashscope.console.aliyun.com/)
- [README.md](artifact/README.md)
- [SETUP.md](artifact/SETUP.md)
- [USAGE.md](artifact/USAGE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown PRD content with supporting command-line and Python usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated PRD output to local Markdown files depending on the selected runner.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
