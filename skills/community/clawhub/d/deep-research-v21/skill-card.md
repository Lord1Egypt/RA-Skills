## Description: <br>
Deep Research Pro v2.1 guides an agent through stepwise in-depth research with research planning, source cards, quality scoring, cross-source synthesis, and cited final reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueylee-dotcom](https://clawhub.ai/user/xueylee-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research-oriented agents use this skill to structure evidence-heavy research workflows, create source cards, compare conflicting findings, and produce final Markdown reports with traceable citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and query terms may be sent to external research websites or APIs. <br>
Mitigation: Avoid confidential or proprietary topics unless external lookup is acceptable for the project. <br>
Risk: The workflow creates local source cards, synthesis files, and final reports that may contain sensitive research material. <br>
Mitigation: Run the skill in a dedicated project folder and remove generated artifacts when they are no longer needed. <br>
Risk: Generated reports can contain incomplete, stale, or low-quality evidence if source collection or quality gates are skipped. <br>
Mitigation: Follow the staged workflow, review source-card quality scores, and verify citations before relying on conclusions. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/xueylee-dotcom/deep-research-v21) <br>
- [Publisher profile](https://clawhub.ai/user/xueylee-dotcom) <br>
- [Research protocol](artifact/RESEARCH_PROTOCOL.md) <br>
- [Quality criteria](artifact/QUALITY_CRITERIA.md) <br>
- [Source card template](artifact/templates/source-card.md) <br>
- [Report template](artifact/templates/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, source-card templates, final reports, and inline shell or Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local research artifacts such as research/plan.md, sources/card-xxx.md, analysis/synthesis.md, and reports/final-report.md.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata, artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
