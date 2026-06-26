## Description: <br>
Academic Paper Reviewer coordinates a seven-agent Hermes workflow for manuscript review, re-review, methodology checks, guided improvement, and reviewer calibration. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255) <br>

### License/Terms of Use: <br>
CC BY-NC 4.0 <br>


## Use Case: <br>
Researchers, authors, editors, and academic reviewers use this skill to generate structured peer-review feedback, editorial decisions, revision roadmaps, and calibration metrics for manuscript review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manuscript drafts and intermediate review outputs may be processed by external model APIs when cross-model behavior or external provider keys are enabled. <br>
Mitigation: Use only with content approved for the chosen provider, and do not enable ARS_CROSS_MODEL or add external API keys for confidential, unpublished, proprietary, or IRB-sensitive material. <br>
Risk: Broad activation language may invoke review behavior in sessions that contain sensitive documents. <br>
Mitigation: Prefer explicit invocation and review the trigger behavior before using the skill in sensitive sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyrenxu7255/academic-paper-reviewer) <br>
- [Original upstream project from metadata](https://github.com/Imbad0202/academic-research-skills) <br>
- [Attribution](artifact/ATTRIBUTION.md) <br>
- [Review criteria framework](artifact/references/review_criteria_framework.md) <br>
- [Quality rubrics](artifact/references/quality_rubrics.md) <br>
- [Statistical reporting standards](artifact/references/statistical_reporting_standards.md) <br>
- [Editorial decision standards](artifact/references/editorial_decision_standards.md) <br>
- [Integration guide](artifact/references/integration_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown review reports, editorial decisions, revision roadmaps, and calibration summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured scores, reviewer findings, action items, and calibration metrics.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
