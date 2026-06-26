## Description: <br>
Translate and analyze academic computer science papers between English and Chinese, summarize content, answer paper-grounded questions, and compare related works. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levinaz69](https://clawhub.ai/user/levinaz69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ingest academic PDFs or arXiv papers, produce English-Chinese academic translations, and answer research questions using extracted paper content with supplementary web research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded, local, or downloaded papers may be extracted and cached under /tmp for multi-turn use. <br>
Mitigation: Avoid confidential or unpublished papers unless temporary paper folders are cleared after the session. <br>
Risk: Supplementary web research can expose paper topics or produce citations that need review. <br>
Mitigation: Disable web search for sensitive papers and review cited sources before relying on answers. <br>


## Reference(s): <br>
- [Academic Translator on ClawHub](https://clawhub.ai/levinaz69/academic-translator) <br>
- [Publisher profile](https://clawhub.ai/user/levinaz69) <br>
- [arXiv](https://arxiv.org/) <br>
- [PyMuPDF](https://pymupdf.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with translated sections, summaries, citations, and JSON emitted by helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use temporary local paper context and web research when answering follow-up questions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
