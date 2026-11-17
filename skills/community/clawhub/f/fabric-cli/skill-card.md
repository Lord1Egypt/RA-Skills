## Description:

Guides agents through safe Fabric.so CLI workflows for setup, search, browsing, saving notes, links, and files, task and workspace management, shell completion, JSON output, and persistent agent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and command-line agents use this skill to operate the Fabric.so CLI for knowledge workspace search, content capture, task management, workspace selection, assistant queries, setup diagnostics, and persistent project memory while respecting consent and secret-handling boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer workflow can execute mutable remote code on the user's machine.

Mitigation: Download and inspect the complete installer before execution, prefer a versioned or signed package when available, and run installation only after explicit user approval.

Risk: Fabric CLI write operations can change a remote workspace.

Mitigation: Confirm the active workspace before writes and require a clear user request for note, link, file, folder, task, workspace, authentication, or other state-changing commands.

Risk: Uploaded files, saved notes, or persistent memory can expose credentials or sensitive information.

Mitigation: Avoid credential-bearing files and secret text, redact tokens from summaries and memory notes, and only save persistent memory when the user has opted in.

## Reference(s):

- [Fabric User Guide CLI Usage](https://user-guide.fabric.so/ai-tools/CLI-usage)
- [Fabric CLI Download](https://fabric.so/download/cli)
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/skills/fabric-cli)
- [Sources and provenance](references/sources.md)
- [Fabric.so CLI command reference](references/command-reference.md)
- [Security and consent guide](references/security-and-consent.md)
- [Fabric.so CLI workflow playbook](references/workflows.md)
- [Using Fabric.so CLI as persistent agent memory](references/agent-memory.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON-oriented command plans, and generated note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for agent execution planning and user-facing summaries; live Fabric CLI results depend on installed CLI version, authentication, workspace, and network access.]

## Skill Version(s):

1.0.0 (source: server release; artifact metadata version 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
