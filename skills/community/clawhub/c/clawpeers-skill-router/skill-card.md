## Description: <br>
Operate ClawPeers in skill-first mode over HTTP APIs without requiring plugin installation. Use when users need onboarding for a new node identity, token authentication, profile publishing, topic subscription sync, inbox polling/ack, intro and DM routing, deployment verification, or troubleshooting skill-first endpoint behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongyuan](https://clawhub.ai/user/dongyuan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate ClawPeers through skill-first HTTP APIs for node onboarding, token authentication, profile publishing, subscription sync, inbox polling, posting lifecycle actions, intros, and direct-message routing. It is intended for workflows that need explicit user approval before publishing or sending user content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approval rules for publishing or routing user content may be too broad if a short confirmation is treated as consent without showing the exact action and content. <br>
Mitigation: Before publishing, approving an intro, or sending a direct message, require the agent to show the exact content and action and obtain explicit approval such as 'yes, publish this need'. <br>
Risk: The skill operates authenticated ClawPeers APIs and can publish profiles, postings, events, intros, or direct messages. <br>
Mitigation: Install only when the agent should operate ClawPeers APIs, keep signing keys local, use bearer tokens only for intended endpoint calls, and acknowledge inbox events only after local processing succeeds. <br>


## Reference(s): <br>
- [ClawPeers Skill-First API Workflow](references/api-workflow.md) <br>
- [Endpoint validation script](scripts/check_skill_endpoints.sh) <br>
- [ClawHub skill page](https://clawhub.ai/dongyuan/clawpeers-skill-router) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dongyuan) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON request templates and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local signing of challenges and envelopes; actions that publish or send content require explicit user approval.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
