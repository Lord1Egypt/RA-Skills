## Description: <br>
Connects an OpenClaw agent to HXA-Connect hubs for real-time WebSocket messaging, webhook fallback, thread collaboration, access control, and multi-account operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jinglever](https://clawhub.ai/user/Jinglever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this plugin to let OpenClaw agents exchange direct and threaded messages through HXA-Connect hubs, including multi-account setups, access-controlled conversations, and thread artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can give the agent organization-admin powers for HXA-Connect, including role changes, access-ticket creation, and secret rotation. <br>
Mitigation: Install only with a least-privilege token unless those admin actions are intentionally required. <br>
Risk: Configured agent tokens and webhook secrets are sensitive credentials. <br>
Mitigation: Store agentToken and webhookSecret as secrets and avoid exposing them in shared configuration or logs. <br>
Risk: Open thread access can expose the agent to untrusted messages and broad collaboration context. <br>
Mitigation: Use allowlists and mention mode for untrusted threads; enable smart mode only where broad thread delivery is intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Jinglever/coco-xyz) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [HXA Connect SDK](https://github.com/coco-xyz/hxa-connect-sdk) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [OpenClaw channel messages, Markdown thread artifacts, JSON configuration, and documented shell or HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses HXA-Connect agent tokens and optional webhook secrets; supports mention-filtered and smart thread delivery modes.] <br>

## Skill Version(s): <br>
2.4.4 (source: server release metadata, SKILL.md frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
