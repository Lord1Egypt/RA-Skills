## Description:

Decodes common error messages and returns likely causes, fixes, and suggestions with multilingual support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honestqiao](https://clawhub.ai/user/honestqiao)

### License/Terms of Use:


## Use Case:

Developers use this skill to interpret common file, port, network, function, and service errors and get concise cause-and-fix guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Responses may not always match the user's preferred language or return a perfectly structured diagnostic object.

Mitigation: Review the returned cause, fix, and language before relying on the guidance, especially for unfamiliar errors.

Risk: Unknown or partial error messages may receive generic guidance instead of a specific fix.

Mitigation: Provide the complete error text and confirm fixes against project logs, documentation, or runtime behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/honestqiao/skills/error-message-decoder)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON-like diagnostic result with error, cause, fix, and suggestion fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Known errors may include language-specific labels; unknown errors receive a generic suggestion to search the exact message.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
