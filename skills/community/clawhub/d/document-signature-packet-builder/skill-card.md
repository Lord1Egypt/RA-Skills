## Description: <br>
Builds a practical sign-here and logistics checklist for a document packet while avoiding legal interpretation and directing the user to confirm issuer rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and administrative teams use this skill to turn document-signing instructions into a checklist for signatures, dates, initials, witnesses, notarization, attachments, copies, deadlines, and submission logistics. It supports packet assembly and issuer-confirmation questions without interpreting legal meaning or advising whether to sign. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake a signing logistics checklist for legal advice or legal validation. <br>
Mitigation: Keep outputs limited to sign-here and logistics support, include the boundary note, and direct users to confirm signing rules with the issuer or a qualified professional. <br>
Risk: Document packets may contain sensitive identity, financial, employment, medical, tax, or real estate information. <br>
Mitigation: Ask only for the minimum needed checklist details, prefer redacted descriptions, avoid full identity numbers, and caution users about cloud storage unless they control encryption, access, MFA, and retention. <br>
Risk: Issuer-specific witness, notary, format, deadline, attachment, or submission requirements may be incomplete or misunderstood. <br>
Mitigation: Use only the user's provided instructions for requirements, mark uncertain items as confirm with issuer, and include a dedicated questions-to-confirm list. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/document-signature-packet-builder) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown checklist with packet summary, sign-here checklist, logistics checklist, issuer-confirmation questions, assembly order, and boundary note] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only output; no code execution, network access, API calls, credentials, or files are required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
