## Description: <br>
Guides an agent through deep research by planning concrete searches, extracting full-text PDF evidence, scoring source quality, checking provenance, comparing conflicting findings, and producing source-backed reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueylee-dotcom](https://clawhub.ai/user/xueylee-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to run structured literature or market research workflows that require full-text source extraction, concrete data capture, quality scoring, conflict analysis, and traceable final reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can download PDFs from supplied research URLs and run local parsing scripts. <br>
Mitigation: Use trusted public PDF URLs only, avoid localhost, private, or internal URLs, and avoid very large files. <br>
Risk: Final research reports can contain unsupported or stale data if the user skips source-card extraction or uses an outdated cutoff date. <br>
Mitigation: Run the sourcing check before report generation, require source-card citations for each data point, and update the report data cutoff date to match the actual sources used. <br>
Risk: Complex card identifiers or incomplete source cards can reduce traceability. <br>
Mitigation: Keep card IDs simple, such as card-001, and exclude sources without confirmed full-text extraction from core conclusions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xueylee-dotcom/deep-research-v22) <br>
- [Research protocol](artifact/RESEARCH_PROTOCOL.md) <br>
- [Quality criteria](artifact/QUALITY_CRITERIA.md) <br>
- [Source card template](artifact/templates/source-card.md) <br>
- [Report template](artifact/templates/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, source cards, research plans, synthesis notes, shell commands, and extracted JSON data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires source-card references for report data points and provenance checks before final report generation.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
