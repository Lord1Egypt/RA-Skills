## Description: <br>
AI-powered bid/tender document review. Extracts text from .docx/.doc files, cross-references bid requirements vs responses, and generates a detailed audit report with risk ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacjiang](https://clawhub.ai/user/zacjiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Bid managers, procurement officers, and quality assurance reviewers use this skill to compare tender requirements against bid responses, extract text from Word documents, and produce a structured audit report with risk-rated findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bid documents and generated review reports may contain confidential procurement or business information. <br>
Mitigation: Use the skill only on documents the user is authorized to review and protect extracted text and generated reports according to the user's confidentiality requirements. <br>
Risk: The skill depends on local Python packages for Word document extraction. <br>
Mitigation: Install python-docx and olefile deliberately, preferably in a virtual environment, before running the extraction scripts. <br>
Risk: The lite version performs text-based review and does not inspect images, seals, certificates, or visual fraud indicators. <br>
Mitigation: Do not treat a clean text review as a complete bid audit when image evidence or visual document integrity is material. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/zacjiang/bid-review-lite) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zacjiang) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with extracted document text and checklist-based findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk ratings, issue locations, impact notes, recommendations, and checklist summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
