## Description:

Open the ClawBuddy LiteKit mission-control dashboard for AI agents - live OpenClaw Gateway status, agent profiles, task board, meeting intelligence, council debates, and AI logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevekaplanai](https://clawhub.ai/user/stevekaplanai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to open a visual ClawBuddy dashboard, inspect OpenClaw agent activity, monitor Gateway health, and follow setup guidance for connecting OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks the user to delegate an OpenClaw API key to hosted Lovable Cloud infrastructure.

Mitigation: Use a dedicated, least-privilege OpenClaw Gateway key, confirm where it will be stored, and revoke it when the integration is no longer needed.

Risk: The status script contacts a Supabase-hosted endpoint using a bundled anonymous token.

Mitigation: Review the script before running it and expect the status check to make a remote request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevekaplanai/skills/clawbuddy-litekit)
- [OpenClaw integration reference](references/openclaw.md)
- [ClawBuddy LiteKit live dashboard](https://agentcommander.lovable.app)
- [OpenClaw Gateway documentation](https://openclaw-openclaw.mintlify.app/concepts/gateway)
- [OpenResponses HTTP API](https://documentation.openclaw.ai/gateway/openresponses-http-api)
- [OpenClaw Agent Protocol](https://openclaw-openclaw.mintlify.app/api/agent-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open an external dashboard and may check a remote hosted status endpoint when the status script is run.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
