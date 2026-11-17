## Description:

Configure, repair, and validate agentmemory integration for Codex App on Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyun2000](https://clawhub.ai/user/yuyun2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure or troubleshoot Agentmemory hooks, context injection, and knowledge graph repair for Codex App on Windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Codex hooks can capture prompts and tool context and send them to the configured Agentmemory service.

Mitigation: Install only with a trusted Agentmemory service, keep AGENTMEMORY_URL on localhost unless the remote service is trusted and protected with authentication and TLS, and review generated hooks before enabling them.

Risk: AGENTMEMORY_SECRET may be stored in Codex configuration or wrapper files used by the hook setup.

Mitigation: Rotate or remove AGENTMEMORY_SECRET if Codex configuration or wrapper files may have been exposed.

Risk: The graph repair workflow can restart services on ports 3111 and 3113 when --restart-service is used.

Mitigation: Use dry-run first and avoid --restart-service unless ports 3111 and 3113 have been confirmed to belong to Agentmemory.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PowerShell, cmd.exe, JSON, and TOML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file changes and validation commands for Windows Codex and Agentmemory setup.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
