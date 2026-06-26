## Description: <br>
Compare two images or PDFs for visual similarity via the PDFAPIHub cloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-workflow teams use this skill to compare images or PDFs for duplicate detection, visual regression checks, template consistency, and near-duplicate analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compared documents and the PDFAPIHub API key are sent to pdfapihub.com for processing. <br>
Mitigation: Use the skill only with documents and credentials that are approved for that provider, and avoid confidential, regulated, or private documents unless the provider and its retention policy are trusted. <br>
Risk: The skill requires a sensitive API key in the CLIENT-API-KEY header. <br>
Mitigation: Store the key in an approved secret manager or environment configuration, rotate it if exposed, and avoid placing real keys in examples, logs, or shared prompts. <br>


## Reference(s): <br>
- [PDFAPIHub Documentation](https://pdfapihub.com/docs) <br>
- [PDFAPIHub API](https://pdfapihub.com/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/document-similarity) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a similarity score, confidence level, and selected comparison method when the hosted API call succeeds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
