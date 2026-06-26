## Description: <br>
帮招聘 HR 快速汇总面试反馈、生成候选人推进话术、整理 Offer 材料并回写跟进记录。 / Help recruiting teams debrief interviews, draft candidate follow-ups, prepare offer materials, and update trackers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashley-aihr](https://clawhub.ai/user/ashley-aihr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, HRBPs, and recruiting operations teams use this skill to turn messy recruiting inputs into interview debriefs, screening recommendations, candidate messages, offer-prep summaries, and tracker updates. It is especially oriented toward China internet-company recruiting workflows where HR needs concise decisions and reusable records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recruiting inputs and generated DOCX, CSV, and JSON outputs may contain confidential HR records. <br>
Mitigation: Install only when authorized to process recruiting data, use a private output directory, and treat all generated files as confidential. <br>
Risk: Generated recommendations, tracker rows, and candidate messages may affect hiring decisions or candidate communications. <br>
Mitigation: Have an HR owner review and approve all recommendations, record updates, and candidate-facing messages before use. <br>
Risk: Local file generation can overwrite same-name files in the selected output directory. <br>
Mitigation: Check the output directory and same-name files before generating DOCX, CSV, or JSON artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ashley-aihr/cn-recruiting-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/ashley-aihr) <br>
- [Project homepage](https://github.com/Ashley-AIHR/hrskill) <br>
- [Real User Scenario](references/real-user-scenario.md) <br>
- [Recruiting Fields Reference](references/recruiting-fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured recruiting records, with optional DOCX, CSV, and JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include normalized_data, decision_summary, missing_information, next_action, message_draft, record_update, and compliance_warning_if_any.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
