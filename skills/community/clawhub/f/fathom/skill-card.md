## Description: <br>
Connect to Fathom AI to fetch call recordings, transcripts, and summaries. Use when user asks about their meetings, call history, or wants to search past conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucassynnott](https://clawhub.ai/user/lucassynnott) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users with Fathom accounts use this skill to list meeting recordings, retrieve transcripts and summaries, search recent calls, and optionally register a webhook for transcript ingestion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript and summary commands can expose private meeting content in the agent session or terminal output. <br>
Mitigation: Use the skill only with meetings the user is authorized to access, treat outputs as confidential, and avoid requesting sensitive transcripts unless necessary. <br>
Risk: Webhook setup can create ongoing delivery of transcripts, summaries, and action items to a supplied HTTPS endpoint. <br>
Mitigation: Run webhook setup only for endpoints the user controls, with trusted storage and retention practices, and remove the webhook when ongoing delivery is no longer needed. <br>


## Reference(s): <br>
- [Fathom AI](https://fathom.video) <br>
- [Fathom Developer Portal](https://developers.fathom.ai) <br>
- [Fathom External API](https://api.fathom.ai/external/v1) <br>
- [ClawHub Fathom Skill Page](https://clawhub.ai/lucassynnott/fathom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown, JSON, plain text, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a Fathom API key supplied through FATHOM_API_KEY or ~/.fathom_api_key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
