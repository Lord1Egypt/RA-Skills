## Description: <br>
Analyze Chinese gaokao application plans across provinces by evaluating score, rank, province-specific admission mode, subject requirements, line margins, major fit, tuition constraints, and transfer-major risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luxinfeng](https://clawhub.ai/user/luxinfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External students, families, and admissions-planning advisors use this skill to evaluate, rank, redesign, or generate Chinese gaokao志愿填报 choices with province-aware risk and major-fit analysis. It helps produce an actionable冲、稳、保、删除/替换 plan while citing public admissions sources and flagging unverifiable data. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Admissions planning may involve sensitive student inputs such as score, rank, subjects, preferences, tuition limits, and uploaded application tables. <br>
Mitigation: Collect only information needed for the analysis and avoid sharing unnecessary personal details in prompts or uploaded files. <br>
Risk: Admissions recommendations can be misleading when policy, enrollment-plan, cutoff, tuition, or subject-requirement data is outdated or not officially verified. <br>
Mitigation: Verify final recommendations against official provincial and university admissions sources, cite sources, and mark unverifiable items as 需复核. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luxinfeng/skills/gaokao-volunteer-risk-skill-cn-adaptive) <br>
- [Admission Mode Reference](policies/admission_modes.md) <br>
- [Input Schema](templates/input_schema.yaml) <br>
- [Report Outline](templates/report_outline.md) <br>
- [Final Verification Checklist](checklists/final_verification.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown report with tables, citations, and checklist items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires official-source citations for web-retrieved admissions data and marks unverifiable items as 需复核.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
