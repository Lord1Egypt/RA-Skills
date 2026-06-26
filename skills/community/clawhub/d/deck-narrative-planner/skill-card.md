## Description: <br>
Converts supplied presentation materials into a structured deck narrative with slide-level titles, evidence needs, transitions, risk framing, and closing actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and presentation authors use this skill to turn goals, audience context, conclusions, and evidence materials into a reviewable PPT or deck storyline. It is suited for reporting, fundraising, and project retrospective workflows where the user needs slide titles, evidence gaps, transitions, risks, and next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inputs may contain sensitive business, project, or personal information. <br>
Mitigation: Use only necessary local materials, redact sensitive content where possible, and avoid feeding confidential data unless it is required for the deck task. <br>
Risk: Generated deck structure may preserve unverified claims or expose missing evidence as if it were ready for presentation. <br>
Mitigation: Review the draft, resolve listed confirmation items, and verify source evidence before using the deck narrative externally. <br>
Risk: The optional Python helper reads selected input material and can write a local Markdown or JSON file. <br>
Mitigation: Run the helper only in a trusted workspace, inspect output paths before writing, and use dry-run or stdout when review-only behavior is preferred. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/52YuanChangXing/deck-narrative-planner) <br>
- [README.md](README.md) <br>
- [resources/spec.json](resources/spec.json) <br>
- [resources/template.md](resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown deck outline or JSON report; optional local output file when the helper script is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local inputs only; the Python helper requires python3 and can write Markdown or JSON to a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
