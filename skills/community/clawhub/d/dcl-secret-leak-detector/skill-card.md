## Description: <br>
Instruction-only runtime secret and credential leak detector for AI agents and LLM pipelines that scans text in the agent context and returns redacted findings with a deterministic DCL audit proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daririnch](https://clawhub.ai/user/daririnch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and AI pipeline operators use this skill to check model outputs, tool results, generated code, retrieved documents, and other agent-visible text for exposed credentials before content reaches users, logs, or downstream systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release advertises capabilities such as wallet, purchase, OAuth, crypto, filesystem, or network access that are not needed for an instruction-only scanner. <br>
Mitigation: Install and run the skill without wallet, purchase, OAuth, filesystem, or network permissions unless a separate review establishes a concrete need. <br>
Risk: Scanning real secrets places those secret values inside the agent context and may expose them to runtime logging or tools. <br>
Mitigation: Use a trusted runtime, limit tool access during scans, avoid persistent logging of scanned content, and keep output limited to redacted samples. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/daririnch/dcl-secret-leak-detector) <br>
- [Fronesis Labs privacy policy](https://fronesislabs.com/#privacy) <br>
- [DCL Security Suite](https://hub.fronesislabs.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON with verdict, hashes, DCL fingerprint, category status, and redacted detections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Raw credential values should not be reproduced; findings use redacted samples and include severity, provider when identifiable, and approximate position.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
