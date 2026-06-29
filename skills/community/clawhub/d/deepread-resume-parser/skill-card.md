## Description: <br>
Parse resumes and CVs into structured JSON for contact information, work history, education, skills, total years of experience, confidence review flags, and optional PII redaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting teams, ATS developers, job boards, and sourcing workflows use this skill to convert resume documents into structured candidate data and route ambiguous fields for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume documents can contain sensitive personal data and are submitted to a third-party API. <br>
Mitigation: Use the skill only with documents approved for DeepRead processing, follow the service's data handling requirements, and use PII redaction when blind screening is needed. <br>
Risk: The skill requires a DeepRead API key. <br>
Mitigation: Store DEEPREAD_API_KEY in the agent's secret store or environment and avoid pasting credentials into prompts, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/uday390/deepread-resume-parser) <br>
- [DeepRead Homepage](https://www.deepread.tech) <br>
- [DeepRead Dashboard](https://www.deepread.tech/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas, API examples, Python code, and cURL commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends resume documents to the DeepRead API for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
