## Description: <br>
Places Stepone AI outbound calls to Chinese phone numbers from a prompt and lets an agent check call status, transcripts, and live conversation streams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ustczz](https://clawhub.ai/user/ustczz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to initiate one confirmed Stepone AI outbound call, then inspect call status, cost, transcripts, or a live SSE conversation stream. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Phone numbers, call instructions, and transcripts are sent to Stepone AI and may be printed in terminal output. <br>
Mitigation: Use the skill only when Stepone AI is trusted for the call data, avoid unnecessary sensitive details, and run transcript commands only in terminals whose output is not logged or visible to others. <br>
Risk: A real outbound call may create cost, compliance, or consent obligations. <br>
Mitigation: Verify the recipient, purpose, authorization, and local rules before typing CALL; use the default one-recipient flow rather than raw API calls. <br>
Risk: STEPONEAI_API_KEY is a sensitive credential. <br>
Mitigation: Provide it only through the environment, keep it out of prompts and logs, and rotate it promptly if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ustczz/ai-phone-calls-steponeai) <br>
- [Stepone AI portal](https://open-skill.steponeai.com) <br>
- [Stepone AI API keys](https://open-skill.steponeai.com/keys) <br>
- [Stepone AI call initiation endpoint](https://open-skill-api.steponeai.com/api/v1/callinfo/initiate_call) <br>
- [Stepone AI call information endpoint](https://open-skill-api.steponeai.com/api/v1/callinfo/search_callinfo) <br>
- [Stepone AI live conversation stream endpoint](https://open-skill-api.steponeai.com/api/v1/callinfo/stream_chat_history) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Text, Guidance] <br>
**Output Format:** [Terminal text, JSON responses, and Server-Sent Events stream lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STEPONEAI_API_KEY and prompts for explicit confirmation before initiating a real call.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
