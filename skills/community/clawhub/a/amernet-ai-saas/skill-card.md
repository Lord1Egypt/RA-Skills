## Description: <br>
Connect your AI SaaS intelligent agent to any messaging channel via OpenClaw, including WhatsApp, Telegram, Slack, Discord, iMessage, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amernet](https://clawhub.ai/user/amernet) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to connect an Amernet AI SaaS chatbot to OpenClaw messaging channels and route user conversations to the selected chatbot while preserving per-channel session context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected-channel messages and user identifiers are sent to an external AI SaaS service. <br>
Mitigation: Limit which channels are connected, notify users where required, and avoid forwarding sensitive or regulated data unless applicable agreements allow it. <br>
Risk: The skill requires an all-permissions API key for the AI SaaS portal. <br>
Mitigation: Store the API key carefully in the OpenClaw environment configuration, restrict access, and rotate the key regularly. <br>


## Reference(s): <br>
- [Amernet AI SaaS ClawHub listing](https://clawhub.ai/amernet/amernet-ai-saas) <br>
- [AI SaaS portal](https://saas.salesbay.ai) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration, Guidance] <br>
**Output Format:** [Text replies with JSON API request guidance and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes channel messages to an external chatbot, supports reset and status commands, and returns a fallback message when the service is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
