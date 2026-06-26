## Description: <br>
Parses academic drafts, extracts topics and keywords, searches for relevant papers through academic-search, asks the user to confirm candidates, and formats or inserts citations for Markdown, LaTeX, and Word documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vigorouspp](https://clawhub.ai/user/vigorouspp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and researchers use this skill to add, format, and insert academic references into drafts after reviewing recommended citation candidates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The citation insertion workflow can modify selected Markdown, LaTeX, or Word documents. <br>
Mitigation: Use an explicit output path or work on a copy of important documents before accepting inserted references. <br>
Risk: Document topics and keywords may be sent to external academic search providers through the academic-search dependency. <br>
Mitigation: Avoid confidential or unpublished drafts when external search disclosure is not acceptable. <br>
Risk: Recommended papers may be irrelevant or unsuitable for the user's argument. <br>
Mitigation: Confirm candidate references before formatting or insertion. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vigorouspp/auto-citation) <br>
- [academic-search dependency](https://github.com/ustc-ai4science/academic-search) <br>
- [Citation style reference](references/citation-styles.md) <br>
- [Workflow examples](references/workflow-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON parser output, formatted citation files, and document updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports BibTeX, GB/T 7714, and APA citation formats for Markdown, LaTeX, and Word workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
