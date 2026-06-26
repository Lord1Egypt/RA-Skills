## Description: <br>
Build Word literature reviews from BibTeX, RIS, CSL JSON, CSV/TSV, or plain reference lists with GB/T 7714, APA, MLA, Chicago, IEEE, Vancouver, or Harvard bibliography formatting and clickable Word REF citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephenlzc](https://clawhub.ai/user/stephenlzc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, students, and researchers use this skill to turn curated literature metadata into Chinese or English Word literature-review DOCX files with numeric REF citations, bibliography formatting, and structural validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated bibliography text, source selection, or citation formatting may be academically inaccurate for a specific institution or publication style. <br>
Mitigation: Manually review the generated bibliography and DOCX for academic accuracy, punctuation, capitalization, and institutional requirements before submission. <br>
Risk: The skill processes user-provided reference files and may write DOCX or temporary outputs. <br>
Mitigation: Provide only source files intended for agent access and choose explicit output paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stephenlzc/bibtex-literature-review) <br>
- [Input formats](references/input-formats.md) <br>
- [Review JSON specification](references/review-json-spec.md) <br>
- [OOXML REF fields](references/ooxml-ref-fields.md) <br>
- [Citation styles](references/citation-styles.md) <br>
- [Workflow](references/workflow.md) <br>
- [Acceptance criteria](references/acceptance.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON contracts, Python command examples, and DOCX generation or validation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or validate DOCX files through bundled scripts when the host agent is asked to create a document.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
