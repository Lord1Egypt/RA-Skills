## Description: <br>
Places AI-assisted outbound calls to Chinese mobile phone numbers through Stepone AI and lets users check call status, transcripts, and live conversation streams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ustczz](https://clawhub.ai/user/ustczz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to initiate one confirmed Stepone AI outbound call at a time, then inspect call status, call details, and live or completed conversation content. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real paid outbound calls. <br>
Mitigation: Confirm authorization, recipient number, and call purpose before typing CALL or RAWCALL. <br>
Risk: Phone numbers, call instructions, and transcripts are sent to Stepone AI. <br>
Mitigation: Use only when the provider is trusted for the call data and avoid unnecessary sensitive personal, financial, or business information in prompts. <br>
Risk: The Stepone AI API key grants access to the calling service. <br>
Mitigation: Keep STEPONEAI_API_KEY private in the environment and rotate it promptly if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ustczz/ai-calls-china-phone) <br>
- [Stepone AI Skill Portal](https://open-skill.steponeai.com) <br>
- [Stepone AI API Base](https://open-skill-api.steponeai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Guidance] <br>
**Output Format:** [Terminal output, JSON responses, and Server-Sent Events] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STEPONEAI_API_KEY and interactive confirmation before placing a call.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
