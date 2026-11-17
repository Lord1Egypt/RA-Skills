## Description:

Interact with aria2 download manager via JSON-RPC 2.0. Manage downloads, query status, and control tasks through natural language commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azzgo](https://clawhub.ai/user/azzgo)

### License/Terms of Use:

MIT

## Use Case:

Developers and power users use this skill to control an aria2 download manager from an agent workflow, including starting downloads, checking status, pausing or resuming tasks, and adjusting download options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles aria2 RPC secrets and may connect to remote RPC hosts.

Mitigation: Prefer localhost or HTTPS/WSS for remote hosts, keep config files owner-only, and avoid committing RPC secrets.

Risk: The skill can perform destructive or broad download actions such as removing downloads, purging results, pausing all downloads, changing global options, or adding torrents.

Mitigation: Require explicit user confirmation and verify target GIDs, options, and torrent or URI inputs before executing those actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/azzgo/skills/aria2-json-rpc)
- [Aria2 official documentation](https://aria2.github.io/)
- [Execution Guide](references/execution-guide.md)
- [Aria2 RPC Methods Reference](references/aria2-methods.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Configuration Guide](CONFIG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include aria2 JSON-RPC results summarized for the user.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter metadata.version is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
