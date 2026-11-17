## Description:

AgentCloud gives AI agents cloud storage for registration, file upload and download, share links, and usage checks across Hermes Agent and OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangzh0202](https://clawhub.ai/user/jiangzh0202)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register an AI agent with AgentCloud, configure API-key access, upload and download files, create expiring share links, and inspect storage usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files are uploaded to the AgentCloud service.

Mitigation: Avoid uploading sensitive files unless the service and account controls are acceptable for the data.

Risk: The AgentCloud API key grants access to the agent storage account.

Mitigation: Store the key in a protected secret store or locked-down config file, prefer environment-based injection, and avoid passing the key on the command line.

Risk: Share links behave like bearer links until they expire.

Mitigation: Use short expiration windows, share links only with intended recipients, and revoke or delete shared files when no longer needed.

Risk: Downloads can write service-provided content to local paths.

Mitigation: Download into a trusted directory, review output filenames and paths, and avoid overwriting important local files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangzh0202/skills/agentcloud)
- [AgentCloud web dashboard](https://agentcloud.traceclaw.cn)
- [AgentCloud API base](https://api.traceclaw.cn/api/v1)
- [AgentCloud API health check](https://api.traceclaw.cn/health)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [agentcloud.py helper script](artifact/scripts/agentcloud.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, Python examples, API endpoint guidance, and helper-script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include API calls, local configuration paths, file identifiers, share links, and storage-plan details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
