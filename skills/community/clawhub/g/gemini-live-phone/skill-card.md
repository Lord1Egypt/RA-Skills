## Description: <br>
Bridge Twilio phone calls to Google Gemini Live API for real-time AI voice conversations. No STT/TTS middleware required. Includes VAD and echo suppression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QuantDeveloperUSA](https://clawhub.ai/user/QuantDeveloperUSA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a FastAPI bridge that connects Twilio phone calls to Google's Gemini Live API for real-time voice conversations, including inbound and outbound call handling, VAD, and echo suppression. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes public call-control features that can place and record phone calls using the operator's Twilio account. <br>
Mitigation: Add authentication to call-control and status endpoints, validate Twilio webhook signatures, restrict destination numbers, and enforce rate limits and quotas before exposing the service. <br>
Risk: Operating the bridge as a public telephony service can create consent and disclosure obligations for AI voice processing and any recording. <br>
Mitigation: Set PUBLIC_URL, TWILIO_ACCOUNT_SID, and TWILIO_FROM to controlled values, then implement clear consent and disclosure practices appropriate for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QuantDeveloperUSA/gemini-live-phone) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_API_KEY and TWILIO_AUTH_TOKEN, plus python3 and uvicorn to run the bridge.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
