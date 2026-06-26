## Description: <br>
AI-powered biomedical manuscript generation with DOCX output for English biomedical research papers and Chinese theses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baronshang-blip](https://clawhub.ai/user/baronshang-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, biomedical writers, and research teams use this skill to turn Chinese drafts or outlines into structured biomedical manuscripts, thesis sections, reference lists, and DOCX-ready content. It is specialized for GBD epidemiology, cohort and registry studies, cross-sectional mediation analyses, pharmacovigilance, and Chinese graduate thesis formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Citation checking may rely on external search services and can expose manuscript topics or reference details. <br>
Mitigation: Install only if external citation checks are acceptable for the intended workflow, and review what information is sent for verification. <br>
Risk: Generated biomedical manuscripts may contain incorrect claims, unverifiable citations, or unwanted citation replacements. <br>
Mitigation: Treat outputs as drafts; verify every PMID and DOI, approve replaced citations, and review biomedical claims before submission or publication. <br>
Risk: DOCX formatting, table or figure numbering, and reference numbering can drift during revisions. <br>
Mitigation: Manually review the final DOCX, reference mapping table, and all numbered cross-references before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baronshang-blip/biomedical-paper-billing) <br>
- [Biomedical paper style guide](references/style-guide.md) <br>
- [Biomedical paper section templates](references/section-templates.md) <br>
- [GBD Results Tool](http://ghdx.healthdata.org/gbd-results-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown, manuscript prose, reference mapping tables, Python DOCX builder snippets, and DOCX file generation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce publication-style DOCX content, Vancouver-style numbered references, and journal or thesis formatting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
