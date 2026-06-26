## Description: <br>
Generate private meeting briefings from Fulcra calendar data with optional CRM notes and web research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Professionals use this skill to prepare for upcoming meetings with concise, private briefings built from Fulcra calendar facts, optional CRM notes, and optional public research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar details, attendee information, CRM notes, locations, and generated briefings can contain private or sensitive information. <br>
Mitigation: Use only the Fulcra and CRM sources the user has configured, keep tokens out of chat, and avoid exposing real meeting details in shared examples or public output. <br>
Risk: Thin or ambiguous context can lead to generic or unreliable meeting briefings. <br>
Mitigation: Fail closed when evidence is insufficient and return a short private diagnostic instead of filler. <br>
Risk: Optional public research can introduce stale or irrelevant context. <br>
Mitigation: Use web research only when requested or when CRM context is too thin, and ground briefing claims in available evidence. <br>


## Reference(s): <br>
- [Fulcra Dynamics](https://fulcradynamics.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown briefing or private diagnostic] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a briefing locally only when the user requests it or an explicit output directory is configured.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
