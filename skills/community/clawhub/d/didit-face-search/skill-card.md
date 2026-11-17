## Description:

Integrate Didit Face Search standalone API to perform 1:N facial search against previously verified sessions, helping detect duplicate accounts, matching faces, blocklist hits, and facial deduplication results with ranked similarity percentages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:


## Use Case:

Developers and identity-platform operators use this skill to integrate Didit's face-search API into account registration, duplicate-account detection, blocklist review, and verification workflows. The skill provides API usage guidance, example requests, and a CLI utility for submitting face images and reviewing returned match data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends face images to Didit and may return sensitive identity and biometric match data.

Mitigation: Install and use only with a lawful basis and user consent; limit storage to necessary fields such as session IDs and similarity scores.

Risk: CLI and API examples can expose full face-search responses in logs or terminal history.

Mitigation: Avoid logging full responses, redact identity fields, and handle returned match details as sensitive identity data.

Risk: The DIDIT_API_KEY grants access to Didit API operations.

Mitigation: Store DIDIT_API_KEY in a managed secret store, restrict access, rotate it when exposed, and never commit it to source control.

Risk: The Face Search API documentation lists saved API requests as enabled by default.

Mitigation: Disable saved API requests in code or API parameters unless retention is explicitly required and approved.

Risk: Free-form vendor_data can contain directly identifying user information.

Mitigation: Use pseudonymous vendor_data values and keep mappings in systems with appropriate access controls.

## Reference(s):

- [Didit Documentation](https://docs.didit.me)
- [Didit Face Search API Reference](https://docs.didit.me/standalone-apis/face-search)
- [Didit Face Search Feature Guide](https://docs.didit.me/core-technology/face-search/overview)
- [ClawHub Skill Page](https://clawhub.ai/rosasalberto/skills/didit-face-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, shell commands, and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DIDIT_API_KEY; outputs may include sensitive face-search match metadata and API JSON.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
