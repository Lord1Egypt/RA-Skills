## Description: <br>
Routes medical and wellness questions into safer boundaries by triaging risk, avoiding diagnosis or treatment overclaims, routing emergencies, encouraging clinician involvement, and minimizing private health data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add medical safety routing to assistants that answer, summarize, triage, draft, or route health-related questions, especially where emergency escalation, clinician referral, and private health data minimization matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical or wellness responses may be mistaken for diagnosis, treatment, dosage, or clinical decision support. <br>
Mitigation: Keep replies general, state uncertainty, and route diagnosis, treatment, medication, and dosage decisions to a qualified clinician or pharmacist. <br>
Risk: Urgent symptoms, self-harm, or crisis messages could be handled as routine advice. <br>
Mitigation: Route emergency warning signs and crisis scenarios to emergency services, crisis support, or immediate medical care. <br>
Risk: Private health data could be exposed in review payloads or repeated in replies. <br>
Mitigation: Use minimal redacted summaries and omit raw records, images, full lab reports, insurance identifiers, private messages, credentials, and unrelated health data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mindbomber/aana-medical-safety-router) <br>
- [README](artifact/README.md) <br>
- [Medical Safety Review Schema](artifact/schemas/medical-safety-review.schema.json) <br>
- [Redacted Medical Safety Review Example](artifact/examples/redacted-medical-safety-review.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with optional structured JSON review payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no dependency installation, command execution, service calls, file writes, or persistent memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata; artifact manifest lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
