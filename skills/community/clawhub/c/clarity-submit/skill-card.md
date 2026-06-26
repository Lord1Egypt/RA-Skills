## Description: <br>
Submit a protein variant hypothesis to Clarity Protocol for validation and folding, and check submission status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarityprotocol](https://clawhub.ai/user/clarityprotocol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers, researchers, and agent builders use this skill to submit protein variant hypotheses to Clarity Protocol and track validation or folding progress from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send protein, variant, rationale, disease, and optional wallet details to Clarity Protocol. <br>
Mitigation: Review each submission before execution and avoid sending confidential unpublished rationale unless disclosure to Clarity Protocol is intended. <br>
Risk: Write access requires a Clarity write key and can create external submissions. <br>
Mitigation: Use CLARITY_WRITE_KEY only when submissions are intended, prefer a scoped write key if available, and remove the key from the environment when write access is no longer needed. <br>


## Reference(s): <br>
- [Clarity Protocol](https://clarityprotocol.io) <br>
- [Clarity Submit on ClawHub](https://clawhub.ai/clarityprotocol/clarity-submit) <br>
- [clarityprotocol publisher profile](https://clawhub.ai/user/clarityprotocol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submissions return hypothesis identifiers, status values, tracking URLs, and validation or folding status summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
