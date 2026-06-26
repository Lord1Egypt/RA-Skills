## Description: <br>
A Markdown framework for AI agents to record, index, and review failure events so lessons from mistakes are retained alongside successful work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sly27](https://clawhub.ai/user/Sly27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI agents, developers, and operators use this skill to maintain a structured FAILURES.md journal, preserve debugging context, and review recurring failure patterns over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Failure journals can accidentally capture secrets, account identifiers, login-session details, or private project information. <br>
Mitigation: Redact sensitive values before recording failures, and review FAILURES.md before sharing or committing it. <br>
Risk: Bundled sample entries may be mistaken for facts about the user's own environment. <br>
Mitigation: Remove or replace sample entries before adopting the journal for a real workspace. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown templates and structured journaling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local failure-recording framework; no executable code or network behavior is included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
