## Description: <br>
Assesses AI system descriptions for a preliminary EU AI Act Annex III high-risk or low-risk classification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bluesbell](https://clawhub.ai/user/Bluesbell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, compliance teams, and auditors use this skill to triage whether a described AI system may fall into an EU AI Act Annex III high-risk category before deeper legal review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered AI system descriptions may be sent to the configured Gemini CLI provider. <br>
Mitigation: Remove confidential business, personal, legal, or regulated details unless the Gemini account and data terms are appropriate for that use. <br>
Risk: The classification is automated and preliminary, so it may be incomplete or unsuitable as legal advice. <br>
Mitigation: Use the output for initial triage and send consequential or ambiguous classifications to qualified legal or compliance review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bluesbell/ai-act-risk-check) <br>
- [Publisher profile](https://clawhub.ai/user/Bluesbell) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text classification with shell output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns HIGH-RISK or LOW-RISK and, when high risk, the applicable Annex III category number.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
