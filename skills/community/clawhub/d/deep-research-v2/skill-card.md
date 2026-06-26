## Description: <br>
Deep Research Pro v2 guides agents through multi-phase research planning, public-source retrieval, quality screening, critical analysis, cross-validation, and structured report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueylee-dotcom](https://clawhub.ai/user/xueylee-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research-focused agents use this skill to conduct structured deep research across academic, industry, policy, and patent sources, then produce traceable reports with evidence grades, limitations, and actionable recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and derived keywords may be sent to external public sources during retrieval. <br>
Mitigation: Avoid confidential or regulated topics unless sources are explicitly limited and approved for the work. <br>
Risk: Reports and source lists are saved locally and may contain sensitive research context. <br>
Mitigation: Choose an appropriate output directory and review generated files before sharing or retaining them. <br>
Risk: Quality gates reduce but do not eliminate incorrect, incomplete, or misleading conclusions. <br>
Mitigation: Verify important conclusions against the cited sources before relying on the generated report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueylee-dotcom/deep-research-v2) <br>
- [Research protocol](artifact/RESEARCH_PROTOCOL.md) <br>
- [Quality criteria](artifact/QUALITY_CRITERIA.md) <br>
- [Report template](artifact/templates/report-template.md) <br>
- [Source card template](artifact/templates/source-card.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, JSON source inventories, source cards, validation matrices, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a structured research directory with plans, source inventories, analysis files, final reports, and revised reports when feedback is provided.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
