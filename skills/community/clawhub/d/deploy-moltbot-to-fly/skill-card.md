## Description: <br>
Deploy Moltbot to Fly.io with persistent storage, secure token authentication, environment secrets, and approved device pairing for web UI access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollaugo](https://clawhub.ai/user/hollaugo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to deploy and maintain a Moltbot gateway on Fly.io, including persistent storage, secrets, authentication, device pairing, updates, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users through creating a public Fly.io deployment and storing API keys as Fly secrets. <br>
Mitigation: Install only after reviewing the deployment target, generated gateway token, and secret values, and consider pinning or reviewing the external repository before deploying secrets. <br>
Risk: Device pairing can grant access to the deployed web UI if the wrong pending device is approved. <br>
Mitigation: Inspect pending devices before approval and approve only the device you recognize with the expected roles and scopes. <br>
Risk: Troubleshooting includes a destructive app-destroy command that can remove the Fly.io app and associated state. <br>
Mitigation: Back up or export needed state before running destructive commands and use them only when rebuilding the deployment is intended. <br>


## Reference(s): <br>
- [Fly.io Documentation](https://fly.io/docs/) <br>
- [Moltbot Official Docs](https://docs.molt.bot/platforms/fly) <br>
- [Clawdbot GitHub](https://github.com/clawdbot/clawdbot) <br>
- [ClawHub Skill Page](https://clawhub.ai/hollaugo/deploy-moltbot-to-fly) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment guidance for Fly.io app setup, secrets, persistent storage, token authentication, device pairing, maintenance, and troubleshooting.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
