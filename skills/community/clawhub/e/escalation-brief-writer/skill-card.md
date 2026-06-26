## Description: <br>
Organizes complex issues into escalation briefs that highlight background, impact, attempted actions, blockers, support needed, and supporting evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support, customer success, incident, and cross-team operations users use this skill to turn raw issue context into reviewable escalation briefs and follow-up checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated briefs may include sensitive customer, incident, or personal data from the user's input. <br>
Mitigation: Redact sensitive material when appropriate and review the generated brief before sending, publishing, or sharing it. <br>
Risk: Incomplete or emotionally framed source material can lead to briefs that blur facts, impact, and requests. <br>
Mitigation: Keep missing information in the pending-confirmation section and preserve the skill's fact, impact, and request separation. <br>
Risk: The optional local helper reads supplied files and may write Markdown or JSON output. <br>
Mitigation: Run it only against intended local files, use dry-run or stdout when appropriate, and inspect generated files before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/escalation-brief-writer) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance, Shell commands] <br>
**Output Format:** [Markdown or JSON escalation brief with reviewable checklists and optional local shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are based on provided local input and should be reviewed before sending, publishing, or acting on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
