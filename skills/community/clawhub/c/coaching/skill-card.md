## Description: <br>
Coaching practice support with session preparation, question generation, client progress tracking, and goal setting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Coaches and coaching practice operators use this skill to prepare sessions, generate coaching questions, track client commitments, support goal setting, and maintain momentum between sessions while keeping client records local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles confidential coaching records and was flagged for broad activation wording and weak file path scoping. <br>
Mitigation: Review before installing with real client information; use explicit client-record requests, avoid path-like client names, and require filename sanitization before relying on it for confidential notes. <br>
Risk: Local coaching notes may contain sensitive client data. <br>
Mitigation: Keep records local, document consent and retention practices, and delete records according to the user's retention policy. <br>
Risk: Generated questions or summaries may be incomplete or unsuitable for a specific coaching relationship. <br>
Mitigation: Use outputs as preparation support only; the coach should review them and retain responsibility for client decisions and coaching judgment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AGIstack/coaching) <br>
- [AGIstack publisher profile](https://clawhub.ai/user/AGIstack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with coaching summaries, question lists, progress notes, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and summarize local client records stored under the coaching memory directory when explicitly invoked.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
