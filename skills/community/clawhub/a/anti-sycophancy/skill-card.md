## Description:

Anti-Sycophancy helps AI coding assistant users reduce agreeable default responses by installing prompt rewriting hooks, critical-response skill behavior, and persistent anti-sycophancy rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding assistant users use this skill to make Claude Code or OpenClaw challenge assumptions, surface counterarguments, and transform confirmatory prompts into more open-ended requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes future agent behavior by installing prompt hooks and long-lived rules.

Mitigation: Install only when anti-sycophancy behavior is intended; review changes to Claude Code or OpenClaw settings, hooks, and persistent rule files, and keep backups so the changes can be removed cleanly.

Risk: Prompt rewriting is textual and may alter the tone or framing of user requests in unintended cases.

Mitigation: Use the verification command after installation and review transformed prompts before relying on the hook in regular workflows.

## Reference(s):

- [Ask Don't Tell: Reducing Sycophancy in Large Language Models](https://arxiv.org/abs/2602.23971)
- [Anti-Sycophancy Design Notes](docs/DESIGN.md)
- [Anti-Sycophancy Installation Guide](docs/INSTALL.md)
- [OpenClaw Sycophancy Prompt Research Playbook](https://github.com/0xcjl/openclaw-playbook/blob/main/docs/003-sycophancy-prompt-research.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install or remove hooks and persistent rule files when the user invokes the skill's management commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
