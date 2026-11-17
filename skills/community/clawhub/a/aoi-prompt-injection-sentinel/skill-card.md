## Description:

Detects and scores prompt injection attempts in text, outputting severity, action, and matched rules without external calls or secret handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use this skill to locally screen text for lightweight prompt-injection indicators and receive a severity, recommended action, reasons, and matched detector rule IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner is a simple heuristic detector and may miss novel, obfuscated, or context-dependent prompt-injection attempts.

Mitigation: Use it as a local screening aid and keep human or policy review in place for higher-risk workflows.

Risk: The JSON result includes a deterministic hash of the input text.

Mitigation: Avoid feeding highly sensitive text unless storing or sharing a local result containing that fingerprint is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edmonddantesj/skills/aoi-prompt-injection-sentinel)
- [Support issues](https://github.com/edmonddantesj/aoi-skills/issues)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON written to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes severity, action, reasons, matched rule IDs, and a deterministic SHA-256 fingerprint of the analyzed input.]

## Skill Version(s):

0.1.2 (source: server release evidence, package.json, and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
