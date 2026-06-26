## Description: <br>
Parses uploaded resume files and extracts structured candidate information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[51mee-com](https://clawhub.ai/user/51mee-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and recruiting workflow operators use this skill to parse user-provided resumes into structured profile data for review, screening, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded resumes and parsed outputs may contain personal data such as phone numbers, email addresses, birthdays, salary expectations, and work history. <br>
Mitigation: Use the skill only with resumes the user has permission to process, and avoid unnecessary storage or sharing of parsed outputs. <br>
Risk: LLM extraction can misread or omit resume details, especially from scanned files or inconsistent formatting. <br>
Mitigation: Review parsed fields before relying on the output for candidate decisions or downstream records. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Structured JSON with a suggested Markdown presentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Extracted fields include contact details, birthday, work history, education, skills, salary expectations, awards, and certificates.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
