## Description:

Check agent config for things that break silently on someone else's machine. Use before publishing or committing a SKILL.md, AGENTS.md, CLAUDE.md or llms.txt, before publishing a skill to ClawHub, when a skill "works on my machine" but not for a teammate, when a skill fails to trigger, or when asked to review agent config. Catches references to files that do not exist, absolute paths under the author's home directory, undeclared CLI dependencies, a frontmatter name that does not match the skill's directory, and two skills whose descriptions are so similar the agent fires the wrong one.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyuga611](https://clawhub.ai/user/hyuga611)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run tenken against agent configuration files before committing or publishing them. It helps identify portability and reliability issues such as broken references, undeclared CLI dependencies, placeholder text, mismatched skill names, and overly similar skill descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned third-party npm CLI.

Mitigation: Install only if comfortable running @hyuga/tenken locally; prefer pinning an audited version or running it in a clean workspace without unnecessary secrets.

Risk: The skill is a hygiene and portability check, not a prompt-injection, malware, or supply-chain scanner.

Mitigation: Use a dedicated security scanner before deployment when those risks matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyuga611/skills/agent-config-lint)
- [tenken homepage](https://github.com/hyuga611/tenken)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration]

**Output Format:** [Markdown with inline bash commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to run an npm CLI; tenken exits 0 when clean, 1 when errors are found, and 2 on bad usage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
