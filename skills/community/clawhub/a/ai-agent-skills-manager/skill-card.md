## Description:

Installs and manages OpenClaw skill packages with an interactive selection interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linshuikeji](https://clawhub.ai/user/linshuikeji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to select and install OpenClaw agent skills, including batch installation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installs unverified third-party skill content into an auto-loaded OpenClaw skill directory.

Mitigation: Review the upstream repository and copied skill contents before use; prefer a pinned commit or signed release.

Risk: Uses a shared /tmp/pskoett-ai-skills path for the clone and install workflow.

Mitigation: Use a private temporary directory or clear and recreate the shared path before installation.

Risk: System-wide installation through /usr/local/bin increases trust requirements for the script.

Mitigation: Avoid the sudo installation path unless system-wide access is required and the script has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linshuikeji/skills/ai-agent-skills-manager)
- [Repository cloned by installer](https://github.com/pskoett/pskoett-ai-skills)
- [Agent Skills specification](https://agentskills.io/specification)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and interactive terminal prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create files under ~/.openclaw/skills and write installation logs when bundled shell scripts are executed.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
