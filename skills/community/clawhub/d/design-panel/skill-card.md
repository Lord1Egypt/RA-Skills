## Description: <br>
Design Panel runs a multi-persona UX/UI review of a live web app, captures visual evidence, cross-votes findings, and outputs a ranked report plus fix plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and product teams use this skill during design milestones to review a live web app through accessibility, brand, conversion, mobile, information architecture, trust, motion, and power-user lenses. It helps prioritize the highest-impact UI changes before handing a fix plan to a human or follow-on implementation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local gstack analytics and invokes external helper commands as part of the review workflow. <br>
Mitigation: Install and run it only in environments where local telemetry files and helper execution are acceptable, and review the skill behavior before use. <br>
Risk: Screenshots, computed page data, findings, and reports may contain sensitive information from authenticated or internal apps. <br>
Mitigation: Avoid sensitive authenticated targets unless local evidence capture is acceptable, and review generated artifacts before committing or sharing them. <br>
Risk: The generated ranked findings and fix plan are recommendations that may be incomplete or wrong. <br>
Mitigation: Have a human review the report and verify fixes before applying, committing, or shipping changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/design-panel) <br>
- [gstack browser tooling](https://github.com/garrytan/gstack) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, schema-versioned Markdown fix plans, and JSON finding and score artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped report and fix-plan files under docs/design-panel/ and may print app startup or handoff guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
