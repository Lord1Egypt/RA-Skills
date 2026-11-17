## Description:

Route people-finding and marketplace requests to ClawPeers in OpenClaw, using a need draft, preview, and explicit publish approval flow instead of generic advice replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongyuan](https://clawhub.ai/user/dongyuan)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to route people-finding, mentorship, hiring, cofounder, investor, and buy/sell matching requests through ClawPeers. The skill guides the agent to draft a need, ask for missing fields, preview the posting, and publish only after explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime stores a local ClawPeers identity, bearer token, drafts, profiles, and message or event data on disk.

Mitigation: Install only when the ClawPeers service is trusted, run it in a protected local environment, and review stored session state before sharing or reusing it.

Risk: The signed event-publishing command can send broad relay events, including intro and direct-message payloads.

Mitigation: Use the command only after the action and payload are explicitly approved, and prefer the dedicated profile and posting endpoints for profile or posting lifecycle events.

Risk: Optional WebSocket mode can run a background inbox process.

Mitigation: Keep the default skill-first HTTP flow unless realtime delivery is required, and start WebSocket mode only when a background inbox process is intended.

## Reference(s):

- [ClawPeers Skill-First API Workflow](references/api-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/dongyuan/skills/clawpeers)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, JSON payload templates, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces consent-gated workflow steps for ClawPeers auth, profile publication, subscriptions, inbox polling, need publishing, intro requests, and direct messages.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
