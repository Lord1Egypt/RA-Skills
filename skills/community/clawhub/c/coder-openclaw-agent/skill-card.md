## Description:

Install and wire a coding-focused OpenClaw sub-agent for background code execution, test-driven edits, bug fixing, small project scaffolding, and small-to-medium data-analysis tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milleniumgenai](https://clawhub.ai/user/milleniumgenai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install and wire a coding-focused OpenClaw sub-agent for background code execution, test-driven edits, bug fixing, small project scaffolding, and small-to-medium data-analysis tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation asks users to clone mutable upstream content, build a Docker image, and register retrieved prompts and configuration without pinning or verification.

Mitigation: Review the upstream repository contents before installing, especially the Dockerfile, workspace-coder prompt pack, agent configuration template, and orchestration guide.

Risk: Using the default branch and coder-sandbox:latest can make later installs differ from the reviewed release.

Mitigation: Check out a specific reviewed commit and tag the sandbox image with that revision before registering it in OpenClaw.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/milleniumgenai/skills/coder-openclaw-agent)
- [OpenClaw agent repository](https://github.com/MilleniumGenAI/coder-openclaw-agent)
- [Root README](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/README.md)
- [Agent config template](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/openclaw/agent-config.template.json)
- [Main to Coder orchestration guide](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/openclaw/main-coder-prompt.md)
- [Runtime inventory](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/docker/RUNTIME.md)
- [Known limits](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/docs/known-limits.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected downstream OpenClaw agent output is strict JSON with SUCCESS, PARTIAL, or FAILURE status.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
