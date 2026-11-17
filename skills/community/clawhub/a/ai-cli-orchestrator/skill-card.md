## Description:

Orchestrates multiple AI CLI tools by detecting available tools, prioritizing them, and switching among them for automation workflows with fallback on errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnatom](https://clawhub.ai/user/cnatom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to coordinate installed AI CLI tools, choose a preferred tool for coding, research, or debugging tasks, and fall back when a selected CLI fails or hits limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad context handoff between AI CLIs can expose private code, secrets, or sensitive diffs.

Mitigation: Use only in repositories where sharing context with the configured providers is acceptable, and add explicit redaction and per-provider approval before forwarding task context.

Risk: The scanner may execute shell startup content and overwrite ~/.ai-cli-config.json.

Mitigation: Review the scanner before use, run it in a controlled environment, and back up or isolate existing AI CLI configuration files.

Risk: The artifact makes local-only and minimal-access security claims that conflict with evidence security guidance.

Mitigation: Treat the release as needing manual security review before installation or use on sensitive projects.

## Reference(s):

- [Ai Cli Orchestrator on ClawHub](https://clawhub.ai/cnatom/skills/ai-cli-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and YAML/JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose executing external AI CLI commands and writing local configuration when the scanner is used.]

## Skill Version(s):

1.0.3 (source: server release evidence and target metadata; artifact documentation states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
