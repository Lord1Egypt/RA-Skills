## Description: <br>
Aios Call App Service helps agents read AIOS ontology and invoke AIOS, OpenClaw, or Forguncy business services with live results through a local CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business-system operators use this skill when an agent must query live AIOS, OpenClaw, or Forguncy data, call ontology-defined commands, or prepare state-changing business actions with user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read from and change live business systems. <br>
Mitigation: Install only where AIOS app invocation is intended and authorized, and require explicit user confirmation before any write, approval, deletion, or other state-changing business action. <br>
Risk: Session identifier instructions are inconsistent between sessionId and topic_id. <br>
Mitigation: Confirm the runtime session identifier before use and stop if the required identifier is missing or ambiguous. <br>
Risk: Incorrect ontology, provider, or parameter selection could produce invalid business-system calls. <br>
Mitigation: Read the current ontology before each invocation, use only the supported provider path, and stop instead of guessing when required runtime parameters or ontology entries are incomplete. <br>


## Reference(s): <br>
- [AIOS application invocation rules](references/invoke-rules.md) <br>
- [AIOS data processing rules](references/data-processing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Analysis] <br>
**Output Format:** [Markdown with inline shell commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include parameter confirmation tables, ontology-source notes, assumptions, missing fields, skipped data, and uncertainty.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
