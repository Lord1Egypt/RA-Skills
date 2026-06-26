## Description: <br>
Compare multiple documents to identify conflicting, missing, or ambiguous fields across contracts, reports, forms, specs, and other document sets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorjenorbulim](https://clawhub.ai/user/dorjenorbulim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agent developers use this skill to compare two or more user-provided documents for consistency. It highlights critical mismatches in dates, amounts, names, identifiers, legal terms, missing fields, and ambiguous values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and locally parses user-provided documents, which may contain confidential, personal, legal, or financial information. <br>
Mitigation: Redact unnecessary secrets, credentials, personal data, and confidential fields before use; process documents locally where possible. <br>
Risk: Generated reports may reproduce sensitive discrepancies or source document values. <br>
Mitigation: Review and redact congruence reports before sharing them outside the intended audience. <br>
Risk: Scanned PDFs, handwritten content, images, charts, and semantic equivalence can be difficult to parse or compare reliably. <br>
Mitigation: Treat OCR, image-derived, handwritten, and semantic comparison results as review cues and confirm material findings manually. <br>


## Reference(s): <br>
- [Document Congruence Checker skill page](https://clawhub.ai/dorjenorbulim/document-congruence-checker) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact agent configuration](artifact/agent-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown discrepancy report with comparison tables, congruence summaries, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local document parsing tools such as pdftotext or docx2txt when available; reports can reproduce sensitive document values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
