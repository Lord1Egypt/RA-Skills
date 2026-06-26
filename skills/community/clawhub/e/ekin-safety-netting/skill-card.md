## Description: <br>
Automated clinical safety netting for NHS GPs. Follows up with patients after appointments, checks for red flag symptoms, escalates to GP when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ekin-kahraman](https://clawhub.ai/user/ekin-kahraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
NHS GP teams use this skill to follow up with patients after appointments, check for deterioration or red flag symptoms, and escalate concerning, unclear, or missing responses for GP review. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive patient communications and records in a clinical follow-up workflow. <br>
Mitigation: Use only in a governed clinical environment with explicit patient consent or another approved legal basis, verified recipient identity, approved communication channels, and defined retention, deletion, audit, encryption, and de-identification rules. <br>
Risk: Automated assessment could affect escalation, resolution, or patient follow-up status. <br>
Mitigation: Require human clinical review for patient messages and status changes, and escalate red flags, unclear responses, and non-responses to the GP. <br>
Risk: The skill requires credentials for communication and patient-data storage services. <br>
Mitigation: Use least-privilege credentials, protect API keys and service-role keys, and restrict database access to the minimum required clinical workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ekin-kahraman/ekin-safety-netting) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Plain-English patient and GP messages with structured status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires governed access to patient contact, safety-net, communication, and audit data.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
