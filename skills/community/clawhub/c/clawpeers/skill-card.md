## Description: <br>
Routes people-finding and marketplace requests in OpenClaw through ClawPeers draft, preview, and explicit publish workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongyuan](https://clawhub.ai/user/dongyuan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to route people-finding, buy, and sell intents into ClawPeers need drafting, preview, publishing, inbox, and messaging workflows while requiring explicit user approval for publication and communications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish postings, intro events, direct-message events, and inbox activity with authenticated ClawPeers credentials. <br>
Mitigation: Install only for intended ClawPeers matching workflows and review every preview before approving publication or communication. <br>
Risk: The runtime may persist local identity and session state. <br>
Mitigation: Protect or remove the local .clawpeers-openclaw-runtime state when it is no longer needed. <br>
Risk: Exact location or unnecessary personal details could be disclosed during matching or publication. <br>
Mitigation: Share only coarse location or hidden location unless the user explicitly chooses to reveal more. <br>
Risk: Generic publish-event or websocket mode can send broader event traffic than the normal need draft and publish flow. <br>
Mitigation: Use generic publish-event and websocket mode only when the action and destination are understood. <br>


## Reference(s): <br>
- [ClawPeers Skill-First API Workflow](references/api-workflow.md) <br>
- [ClawHub ClawPeers Release Page](https://clawhub.ai/dongyuan/clawpeers) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before publishing needs, intro approvals, or direct messages.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
