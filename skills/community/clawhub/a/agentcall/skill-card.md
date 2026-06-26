## Description: <br>
AgentCall lets agents provision phone numbers, send and receive SMS, place voice calls, configure inbound and outbound AI voice calls, manage call memory, and use related AgentCall API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kintupercy](https://clawhub.ai/user/kintupercy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an AI agent controlled access to AgentCall telephony workflows, including phone number provisioning, SMS, OTP extraction for apps they control, AI receptionists, outbound AI calls, schedules, webhooks, and call memory. It is intended for users who are prepared to manage real recipients, paid usage, credentials, and privacy-sensitive call data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger real SMS messages, voice calls, outbound AI calls, and callbacks to real people. <br>
Mitigation: Confirm the recipient, purpose, message or prompt, and user authorization before any external communication. <br>
Risk: Several actions can create recurring or per-minute costs, including phone numbers, AI voice, Premium Voice, recording, and proactive schedules. <br>
Mitigation: Confirm the plan, expected budget, billing mode, rates, and scope before invoking billable actions; monitor usage after persistent configurations are enabled. <br>
Risk: Inbound AI, schedules, webhooks, and memory settings can keep operating after initial setup. <br>
Mitigation: Confirm persistent settings up front, review them after setup, and disable or cancel them when the stated need has ended. <br>
Risk: Call recording and call memory may involve sensitive personal or business information. <br>
Mitigation: Use recording only after explicit opt-in, disclose recording where appropriate, and limit memory or webhook configuration to contexts the user has approved. <br>
Risk: The skill requires sensitive AgentCall credentials and can optionally handle customer-supplied provider keys for BYOK voice billing. <br>
Mitigation: Use environment variables or approved secret storage, avoid exposing key values in conversation, and confirm BYOK mode changes before storing or removing provider keys. <br>


## Reference(s): <br>
- [ClawHub AgentCall skill page](https://clawhub.ai/kintupercy/agentcall) <br>
- [Publisher profile](https://clawhub.ai/user/kintupercy) <br>
- [AgentCall API plain-text reference](https://api.agentcall.co/llms.txt) <br>
- [AgentCall pricing](https://agentcall.co/#pricing) <br>
- [AgentCall voice prompt guide](https://agentcall.co/docs/voice-prompts) <br>
- [AgentCall post-call webhook guide](https://agentcall.co/docs/post-call-webhook) <br>
- [AgentCall Hermes walkthrough](https://agentcall.co/docs/hermes) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown guidance with API paths, JSON request examples, curl commands, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated AgentCall API calls that affect real phone numbers, SMS, voice calls, webhooks, schedules, recordings, and memory settings.] <br>

## Skill Version(s): <br>
2.12.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
