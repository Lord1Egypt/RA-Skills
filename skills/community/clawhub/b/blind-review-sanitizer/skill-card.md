## Description: <br>
One-click removal of author names, affiliations, acknowledgments, and excessive self-citations from manuscripts to meet double-blind peer review requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googolme](https://clawhub.ai/user/googolme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, authors, and editorial support teams use this skill to create blinded manuscript versions for double-blind peer review while preserving document structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes manuscripts that may contain author identities, affiliations, emails, phone numbers, acknowledgments, and other sensitive submission details. <br>
Mitigation: Run the skill only on manuscript copies, limit access to generated outputs and audit notes, and treat terminal summaries as sensitive. <br>
Risk: Automated anonymization can miss identifiers in metadata, figures, supplementary files, or unusual phrasing. <br>
Mitigation: Manually review the sanitized manuscript, clear document metadata separately, and check supplementary materials before submission. <br>
Risk: Pattern-based redaction can over-redact legitimate content or alter citation context. <br>
Mitigation: Use highlight or review workflows first when possible, then verify citation integrity and document formatting before using the blinded output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googolme/blind-review-sanitizer) <br>
- [COPE Guidelines for Peer Review](https://publicationethics.org/resources/guidelines) <br>
- [IEEE Publications Rights and Responsibilities](https://www.ieee.org/publications/rights/index.html) <br>
- [ACM Policy on Authorship](https://www.acm.org/publications/policies/authorship) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Sanitized DOCX, Markdown, or plain text files with terminal summaries and audit notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redaction placeholders such as [AUTHOR NAME], [INSTITUTION], [EMAIL], [ACKNOWLEDGMENTS REMOVED], [SELF-CITE: ...], and [PREVIOUS WORK].] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
