## Description: <br>
Gives an agent a real phone number for receiving calls, calling users back, running scheduled briefings, and placing third-party calls through ClawCall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawcall](https://clawhub.ai/user/clawcall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an OpenClaw agent to phone calls through ClawCall, including inbound conversations, callbacks, scheduled briefings, and third-party calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Callers, scheduled phone flows, and third-party call flows may reach agent context and outbound calling features. <br>
Mitigation: Use only with trusted callers and require explicit approval for third-party, scheduled, paid, recorded, and callback calls. <br>
Risk: Call handling can expose account credentials, local user profile data, memory, tasks, schedules, call audio, transcripts, and generated replies. <br>
Mitigation: Protect CLAWCALL_API_KEY and CLAWCALL_EMAIL, avoid placing secrets in USER.md, MEMORY.md, tasks, or call objectives, and assume ClawCall, Twilio, and any configured model backend may process call data. <br>
Risk: The local bridge and CLI fallback increase local runtime exposure if misconfigured. <br>
Mitigation: Keep the bridge bound to 127.0.0.1, prefer HTTP bridge mode, avoid the Windows CLI fallback, and stop stale bridge or listener processes before restarting. <br>


## Reference(s): <br>
- [ClawCall Phone on ClawHub](https://clawhub.ai/clawcall/clawcall-phone) <br>
- [ClawCall Homepage](https://clawcall.com) <br>
- [ClawCall Backend and Agent Setup Reference](references/setup.md) <br>
- [ClawCall API](https://api.clawcall.online) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, HTTP API calls, and Node.js runtime scripts that return JSON responses for phone turns.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, openclaw, CLAWCALL_API_KEY, and CLAWCALL_EMAIL; the preferred runtime uses a local HTTP bridge bound to 127.0.0.1.] <br>

## Skill Version(s): <br>
2.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
