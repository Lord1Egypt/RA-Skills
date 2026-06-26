## Description: <br>
Saves, lists, and restores session or project context summaries as local Markdown files so users can resume work across account switches, cleared sessions, or new conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bayllech](https://clawhub.ai/user/bayllech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to preserve working context in local session slots or project summaries and later restore the concise state, decisions, files, commands, risks, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local handoff summaries can accidentally include secrets, credentials, or sensitive personal data. <br>
Mitigation: Review summaries before saving and omit tokens, keys, cookies, full account credentials, and unnecessary sensitive details. <br>
Risk: Reusing a session slot or project name overwrites the previous local summary. <br>
Mitigation: Use clear, specific slot or project names and confirm the target before saving when prior context should be preserved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bayllech/context-handoff) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown summaries and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local session summaries under handoffs/sessions/<slot>.md and project summaries under projects/<project-name>.md when requested.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
