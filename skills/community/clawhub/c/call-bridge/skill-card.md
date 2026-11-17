## Description: <br>
Call Bridge helps an agent place and manage real phone calls, including parallel outbound calls, live handoff, inbound call preferences, voice settings, and call follow-up state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to have an agent collect information by phone, compare options across multiple businesses, configure inbound handling, or bridge the user into live calls when human approval or sensitive decisions are needed. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to place real phone calls and bridge the user into live calls. <br>
Mitigation: Require explicit confirmation before every call or handoff, including the phone number, purpose, participant, and allowed commitments. <br>
Risk: Live calls, inbound forwarding, and transcript reuse can create consent and privacy exposure. <br>
Mitigation: Confirm participant consent where required, limit transcript retention, and reuse transcript content only when it is necessary for the user's stated task. <br>
Risk: Call Bridge credentials and sign-in URLs can expose account access if stored or logged unsafely. <br>
Mitigation: Use trusted credential storage, avoid placing keys or tokens in logs or shared files, and restrict local credential-file permissions. <br>
Risk: The server security summary says the documentation lacks clear safeguards for consent, live calls, credentials, and transcript reuse. <br>
Mitigation: Review the skill carefully before installation and set strict operating limits for calls, handoffs, credential handling, and transcript replay. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/call-bridge) <br>
- [Call Bridge API](https://api.call-bridge.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and bash/curl command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API calls, call summaries, transcript-derived follow-up state, and configuration instructions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
