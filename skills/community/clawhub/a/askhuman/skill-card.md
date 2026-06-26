## Description: <br>
Human Judgment as a Service for AI agents. Preference, tone, and trust validated by real people. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hagiss](https://clawhub.ai/user/hagiss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use AskHuman to request real human judgment for subjective decisions, verification, content moderation, aesthetic choices, and feedback during agentic workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task prompts, attachments, and surrounding context may be sent to AskHuman and external human reviewers. <br>
Mitigation: Do not submit secrets, credentials, regulated personal data, or proprietary material unless organizational policy permits it. <br>
Risk: The security review notes broad local read/network command authority and unsafe API-key handling examples. <br>
Mitigation: Review commands before execution, keep API keys in environment variables, avoid embedding keys in URLs where possible, and prefer versions with narrower tool permissions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hagiss/askhuman) <br>
- [Developer Docs](https://askhuman.guru/developers) <br>
- [API Reference](askhuman/references/API-REFERENCE.md) <br>
- [OpenAPI Specification](https://askhuman-api.onrender.com/v1/openapi.json) <br>
- [AskHuman API Base](https://askhuman-api.onrender.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with curl examples and text results returned from AskHuman tasks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return human-submitted answers after polling or Server-Sent Events; tasks can include choice, rating, text, verify, attachment, and optional paid escrow flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata, claw.json, and plugin.json; root SKILL.md frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
