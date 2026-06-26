## Description: <br>
Extracts structured data from contracts, legal agreements, court filings, and compliance documents, with pre-built schemas for parties, clauses, dates, obligations, and PII redaction for privilege review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal, compliance, and operations teams use this skill to extract parties, dates, clauses, obligations, signatures, and other structured fields from legal documents, and to redact sensitive information before external sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Legal-document uploads may contain privileged, regulated, confidential, or client materials. <br>
Mitigation: Confirm that use of the third-party DeepRead API is authorized for the matter or organization before uploading documents. <br>
Risk: Document processing depends on a third-party service and its data handling practices. <br>
Mitigation: Review vendor retention policy, access controls, and contractual approvals before use. <br>


## Reference(s): <br>
- [DeepRead homepage](https://www.deepread.tech) <br>
- [DeepRead dashboard](https://www.deepread.tech/dashboard) <br>
- [DeepRead BYOK setup](https://www.deepread.tech/dashboard/byok) <br>
- [ClawHub skill page](https://clawhub.ai/uday390/deepread-legal) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON schemas, Python examples, and cURL commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends user-provided documents to the DeepRead API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
