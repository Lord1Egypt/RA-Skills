## Description: <br>
Clinical Case Writer drafts Chinese clinical case reports from de-identified patient records and formats them as GB/T 7713.2-2022 Word documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanqing203](https://clawhub.ai/user/fanqing203) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians, medical writers, and agents preparing Chinese clinical case reports use this skill to transform de-identified patient materials into GB/T 7713.2-2022-compliant Markdown and Word drafts with literature-search guidance and reference checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive patient information may be exposed through prompts, filenames, generated documents, or external literature-search terms. <br>
Mitigation: Use only de-identified, authorized patient materials; remove real names, record numbers, dates, and other identifiers; review CNKI and PubMed queries before sending them. <br>
Risk: Generated clinical content, reference choices, and formatting may be inaccurate or unsuitable for submission without review. <br>
Mitigation: Have qualified clinical or editorial reviewers verify the case narrative, source literature, reference metadata, and Word formatting before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fanqing203/clinical-case-writer) <br>
- [README](artifact/README.md) <br>
- [Examples](artifact/examples.md) <br>
- [Word Generation Script](artifact/scripts/clinical_case_writer.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown clinical case report plus Word .docx document; optional text validation report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies GB/T 7713.2-2022 formatting, reference-count checks, and Word superscript handling for in-text citations.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
