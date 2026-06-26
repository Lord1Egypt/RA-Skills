## Description: <br>
AI Company CISO is a security-governance advisor for STRIDE threat modeling, incident response, compliance review, zero-trust controls, AI gateway oversight, NHI policy, and executive crisis approval workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security, governance, and incident-response teams use this skill to draft CISO-style assessments, approval guidance, risk mitigations, crisis response controls, and compliance review recommendations for AI company workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes automatic containment and executive crisis actions that could affect real systems if connected to operational APIs without approved playbooks. <br>
Mitigation: Before deployment, define who can approve containment, which systems may be isolated or shut down, and how rollback and audit review work. <br>
Risk: Broad routing and inconsistent approval limits could create unclear authority during crisis workflows. <br>
Mitigation: Document the approval chain, CEO timeout escalation rules, CISO or dual-approval requirements, and white-listed operations before granting production access. <br>
Risk: The release is tagged as requiring sensitive credentials. <br>
Mitigation: Use least-privilege scoped credentials and keep production credentials unavailable until the skill and incident-response workflow have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnsmithfan/ai-company-ciso-2-0-0) <br>
- [STRIDE assessment for CEO-EXEC crisis channel](references/stride-assessment-crisis-channel.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or structured security assessment, incident response, and risk mitigation sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe approval workflows, containment choices, audit expectations, and rollback considerations for security governance.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
