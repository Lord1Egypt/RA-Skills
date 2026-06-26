## Description: <br>
审核质检技能 - 自动化质量评估和人工审核工作流。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JEyeshield](https://clawhub.ai/user/JEyeshield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ad production teams and operators use this skill to record automated checks, manual review decisions, quality scores, issue resolution, batch approvals or rejections, and review statistics for advertising materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated quality scores are placeholder mock results and may not reflect real material quality or compliance. <br>
Mitigation: Treat automated scores as advisory only and require human review or an independently validated checker before making approval, rejection, or compliance decisions. <br>
Risk: Batch workflows can create many approval or rejection records for specified materials. <br>
Mitigation: Use batch approval and rejection only with explicit task and material IDs, and review the affected materials before submitting the batch action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JEyeshield/ad-production-review-quality) <br>
- [Publisher profile](https://clawhub.ai/user/JEyeshield) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, guidance] <br>
**Output Format:** [Structured command responses with review records, quality check results, status messages, events, and statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns material and task identifiers, review IDs, scores, pass/fail decisions, issue lists, suggestions, and aggregate counts when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
