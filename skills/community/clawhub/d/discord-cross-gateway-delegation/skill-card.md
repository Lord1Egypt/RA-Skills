## Description: <br>
Set up and operate full cross-gateway task delegation between two OpenClaw Discord bots across different PCs/gateways. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jini92](https://clawhub.ai/user/jini92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up a private Discord delegation lane where a controller OpenClaw bot sends structured tasks to a worker bot on another gateway and relays final results back to the original DM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated DM requests may forward sensitive or unnecessary personal data to another bot or system. <br>
Mitigation: Use the skill only with controlled bots and private lanes, disclose delegated forwarding to users, and avoid forwarding secrets or unnecessary personal data. <br>
Risk: Broad or ambiguous DM triggers could delegate requests unintentionally. <br>
Mitigation: Configure narrow trigger phrases and keep non-matching DM messages on the normal conversation path. <br>
Risk: Public or misconfigured Discord channels could expose internal task traffic. <br>
Mitigation: Use a private delegation lane and verify bot, guild, channel, and allowlist permissions before using real tasks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jini92/discord-cross-gateway-delegation) <br>
- [Setup Checklist](references/setup-checklist.md) <br>
- [Operating Modes](references/operating-modes.md) <br>
- [Full Process](references/full-process.md) <br>
- [Secondary Worker Rollout](references/macjini-rollout.md) <br>
- [Diagnosis](references/diagnosis.md) <br>
- [Task Protocol Examples](examples/task-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured Discord task-envelope examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup checklists, protocol envelopes, operating guidance, and troubleshooting steps; it does not produce executable code.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
