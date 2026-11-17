## Description:

Connect to remote ACP server and execute commands via imclaw-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallnest](https://clawhub.ai/user/smallnest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect an agent to a remote ACP server, run one-shot prompts, continue sessions, and configure remote execution with optional authentication and tool restrictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports remote agent command execution, including modes that can approve broad command access.

Mitigation: Use authenticated wss:// connections, restrict --allowed-tools and --cwd, and avoid --approve-all except in tightly controlled sandboxes.

Risk: Dependency setup may run unverified external code or install latest global packages.

Mitigation: Review installation scripts, pin dependency versions, and prefer verified artifacts before use in production environments.

Risk: Authentication tokens may be exposed if stored broadly in shell startup files or reused across environments.

Mitigation: Use scoped tokens, avoid long-lived secrets in shell profiles, and rotate credentials after testing or incident response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallnest/skills/acp-remote)
- [IMClaw project homepage](https://github.com/smallnest/imclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include text, JSON, or quiet command output when using imclaw-cli output format options.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
