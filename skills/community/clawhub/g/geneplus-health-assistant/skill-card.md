## Description: <br>
Collects structured health information, sends the conversation context to an external medical model API, and returns a structured personalized health risk assessment report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lantian888](https://clawhub.ai/user/lantian888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to provide demographic, medical history, medication, allergy, lifestyle, and lab-result information for a health risk assessment. The agent guides information collection, forwards the full conversation context to the configured model service, and can generate an HTML report from returned assessment data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive health and identity information, including prior conversation context, to external services. <br>
Mitigation: Use only with explicit user consent, minimize shared history and personal data, and disclose the external services involved before transmission. <br>
Risk: Credential handling includes a documented API key and runtime token retrieval through a subprocess call. <br>
Mitigation: Remove exposed credentials, rotate any affected keys, and use a managed secret store or environment-based credential flow. <br>
Risk: Generated HTML reports may contain sensitive health information and the storage and deletion behavior is not fully explained. <br>
Mitigation: Tell users where reports are stored, how to delete them, and sanitize report content before writing or opening HTML files. <br>


## Reference(s): <br>
- [API documentation](references/api_docs.md) <br>
- [ClawHub release page](https://clawhub.ai/lantian888/geneplus-health-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, HTML files, guidance, configuration] <br>
**Output Format:** [Conversational text and Markdown, with optional generated HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Streams API responses and preserves returned report content; optional reports are written as local HTML files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
