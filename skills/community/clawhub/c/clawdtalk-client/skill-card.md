## Description: <br>
ClawdTalk enables voice calls, SMS messaging, and AI Missions for Clawdbot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dcasem](https://clawhub.ai/user/dcasem) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use ClawdTalk to connect an OpenClaw or Clawdbot agent to phone calls, SMS, and outbound outreach missions through ClawdTalk and Telnyx. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration gives a remote voice and SMS service a broad path into the user's main agent with weak approval boundaries. <br>
Mitigation: Restrict the tools exposed to voice and SMS sessions, and require an independent confirmation step before destructive, financial, or otherwise sensitive actions. <br>
Risk: Voice transcripts, SMS content, mission data, and tool results may be sent to ClawdTalk or Telnyx services. <br>
Mitigation: Use the skill only when the operator trusts those services with the relevant conversation and mission data. <br>
Risk: API keys or gateway credentials may be exposed if stored directly in local configuration files. <br>
Mitigation: Prefer environment variables or a secret store for CLAWDTALK_API_KEY and related gateway credentials. <br>
Risk: Custom server URLs can redirect sensitive traffic to an untrusted endpoint. <br>
Mitigation: Avoid custom ClawdTalk server URLs unless the operator controls and trusts the endpoint. <br>


## Reference(s): <br>
- [ClawdTalk ClawHub page](https://clawhub.ai/dcasem/clawdtalk-client) <br>
- [ClawdTalk client homepage](https://github.com/team-telnyx/clawdtalk-client) <br>
- [ClawdTalk service](https://clawdtalk.com) <br>
- [Telnyx](https://telnyx.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with shell commands, JSON configuration examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWDTALK_API_KEY, local skill configuration, and a running OpenClaw or Clawdbot gateway.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
