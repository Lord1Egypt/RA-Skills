## Description: <br>
Competition Assistant helps college students generate competition calendars and find teammates using recognized competition references and local matchmaking records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and education-focused assistants use this skill to look up university competition schedules, build near-term event calendars, and manage teammate requests for matching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Matchmaking records may persist locally across sessions and include raw student contact details. <br>
Mitigation: Ask for explicit consent before saving matchmaking data, store only the minimum needed contact information, and provide clear deletion or expiry controls. <br>
Risk: Match recommendations may expose contact details more broadly than users expect. <br>
Mitigation: Return only sanitized match results, mask contact data by default, and reveal direct contact details only when users have agreed to share them. <br>


## Reference(s): <br>
- [Competition list reference](references/competitions.md) <br>
- [Teaming schema reference](references/teaming-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/smallkeyboy/competition-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown tables and guidance, with JSON from the local teaming script when invoked] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local matchmaking records under ~/.openclaw/workspace/memory/teaming-requests.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
