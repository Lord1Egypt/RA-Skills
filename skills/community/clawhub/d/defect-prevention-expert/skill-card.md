## Description: <br>
Defect Prevention Expert helps teams run lifecycle quality assurance across requirements, design, coding, testing, release, and operations by producing risk, review, metric, and improvement outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengqch](https://clawhub.ai/user/zengqch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and delivery teams use this skill to route quality-assurance work to the right prevention, review, measurement, or improvement workflow and produce stage-specific findings before and after release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill has broader write and command authority than its documented QA tasks clearly need. <br>
Mitigation: Review requested file writes and command execution before approving them, and run the skill only in workspaces where report creation and local knowledge-base updates are acceptable. <br>
Risk: Generated quality findings or process updates may be incorrect or too broad for the target project. <br>
Mitigation: Treat reports, checklist changes, and improvement plans as review drafts until project owners validate the findings and proposed actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zengqch/defect-prevention-expert) <br>
- [Quality Gate Workflow](docs/quality-gate-workflow.md) <br>
- [Review Checklist](checklists/review-checklist.md) <br>
- [Stage Output Templates](templates/stage-output-templates.md) <br>
- [Examples](examples.md) <br>
- [Test Report V3](TEST_REPORT_V3.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Markdown reports, checklists, risk lists, review findings, measurement summaries, and improvement plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose writing report files or updating local quality-knowledge artifacts when the user approves.] <br>

## Skill Version(s): <br>
4.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
