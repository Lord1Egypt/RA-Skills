## Description: <br>
AI-powered cross-border data compliance review agent that analyzes documents, matches regulations such as GDPR, CCPA, and PIPL, identifies risks, and generates actionable compliance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pillarscreation](https://clawhub.ai/user/pillarscreation) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, startups, and compliance teams use this skill as a blueprint for agents that review privacy policies, data processing agreements, and SDK terms against cross-border data rules, then produce risk findings and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes review of legal, vendor, and personal-data documents, which may contain sensitive regulated information. <br>
Mitigation: Use only with appropriate authorization; redact uploads where possible and confirm private processing, encryption, access controls, retention, deletion, and third-party service handling before real use. <br>
Risk: The evidence security summary says sensitive review activity and outputs are permanently stored without clear retention or deletion controls. <br>
Mitigation: Do not process production documents until retention duration, deletion options, audit-log scope, and storage controls are documented and acceptable. <br>
Risk: Generated compliance reports can be incomplete or legally incorrect if regulations, model outputs, or source documents are misread. <br>
Mitigation: Treat reports as decision-support drafts and require review by qualified legal or compliance staff before business or regulatory reliance. <br>


## Reference(s): <br>
- [Datacomply Shield ClawHub release page](https://clawhub.ai/pillarscreation/datacomply-shield) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with architecture diagrams, YAML and Python examples, deployment commands, and report-output descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes bilingual English and Chinese compliance reports and JSON, PDF, and Word report outputs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
