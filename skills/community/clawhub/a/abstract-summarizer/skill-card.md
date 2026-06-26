## Description: <br>
Transform lengthy academic papers into concise, structured 250-word abstracts capturing background, methods, results, and conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and research-support teams use this skill to turn papers, theses, technical reports, pasted text, PDFs, or paper URLs into concise structured abstracts for literature review, submission drafting, relevance screening, or annotated bibliography work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL mode fetches remote paper content and may contact external sites with sensitive or embargoed research URLs. <br>
Mitigation: Prefer local files or pasted text for sensitive material, and use outbound network limits when URL fetching is not required. <br>
Risk: The release uses unpinned Python dependencies for PDF parsing and URL fetching. <br>
Mitigation: Pin and review dependency versions before installing or deploying the skill. <br>
Risk: Generated abstracts can misstate statistics, omit nuance, or overstate conclusions if the source extraction or summarization is imperfect. <br>
Mitigation: Require human review against the original source, especially for numbers, statistical significance, safety findings, and conclusions. <br>


## Reference(s): <br>
- [Abstract Templates by Discipline](references/abstract-templates.md) <br>
- [Evaluation Rubric for Abstract Quality](references/evaluation-rubric.md) <br>
- [Example Abstracts for Computer Science and Biomedical Papers](references/example-abstracts/cs-and-biomed-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files] <br>
**Output Format:** [Structured abstract text or Markdown with Background, Objective, Methods, Results, Conclusion, and word count sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets a 250-word structured abstract and may write the generated abstract to an output file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
