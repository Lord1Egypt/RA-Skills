## Description:

Funky Fund Flamingo is a local repair-first evolution skill for OpenClaw that analyzes session logs, memory, and installed skills to generate measurable mutation directives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icemastert](https://clawhub.ai/user/icemastert)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to inspect OpenClaw session logs, memory, and installed skills, then produce repair-first mutation plans and local evolution state for measurable agent improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gathers private local context, including session logs, USER.md, MEMORY.md, installed skill metadata, and optional environment-derived process variables, to build prompts.

Mitigation: Install only in workspaces where that local context may be read, and review or redact generated prompts before routing them through any cloud-backed agent.

Risk: The skill strongly directs an agent toward file edits by default.

Mitigation: Prefer --review for significant changes, use --dry-run for prompt generation only, and inspect proposed edits before applying them.

Risk: Using the skill through an OpenAI, OpenRouter, or other cloud-model agent can send generated prompts containing local context to that provider.

Mitigation: Keep execution local when sensitive context is present, or review and redact prompts before sending them to a cloud model.

Risk: Installing with a floating @latest package can change installer behavior over time.

Mitigation: Pin the installer version for repeatable installs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/icemastert/skills/funky-fund-flamingo)
- [SKILL.md](SKILL.md)
- [README.md](README.md)
- [ADL.md](ADL.md)
- [VFM.md](VFM.md)
- [TREE.md](TREE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text prompts with local JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local session logs, memory, USER.md, installed skill metadata, and optional environment-derived settings; writes evolution state and optional prompt artifacts under the configured memory directory.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.0.35)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
