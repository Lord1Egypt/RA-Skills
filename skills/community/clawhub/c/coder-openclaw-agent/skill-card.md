## Description: <br>
Install and wire a coding-focused OpenClaw sub-agent for background code execution, test-driven edits, bug fixing, small project scaffolding, and small-to-medium data-analysis tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MilleniumGenAI](https://clawhub.ai/user/MilleniumGenAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and configure a coding-focused sub-agent for background code execution, test-driven edits, bug fixing, project scaffolding, and small-to-medium data-analysis tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill wires a powerful coding sub-agent that can execute code in an OpenClaw sandbox. <br>
Mitigation: Review the linked repository, Dockerfile, agent configuration, and runtime prompt before installing; use an isolated workspace and validate OpenClaw sandbox settings. <br>
Risk: Provider configuration may expose task data to the configured OpenAI Codex provider profile. <br>
Mitigation: Avoid mounting secrets or sensitive directories, watch provider data exposure, and remove the openclaw.json agent entry when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/MilleniumGenAI/coder-openclaw-agent) <br>
- [Repository Homepage](https://github.com/MilleniumGenAI/coder-openclaw-agent) <br>
- [Root README](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/README.md) <br>
- [Agent Config Template](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/openclaw/agent-config.template.json) <br>
- [Main to Coder Orchestration Guide](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/openclaw/main-coder-prompt.md) <br>
- [Runtime Inventory](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/docker/RUNTIME.md) <br>
- [Known Limits](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/docs/known-limits.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation, validation, and smoke testing for an OpenClaw coding sub-agent.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
