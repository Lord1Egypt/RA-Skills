## Description:

Estimates a person's age from a facial image via the Didit standalone API for age gates, compliance checks, underage-user detection, and passive liveness checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:


## Use Case:

Developers and compliance teams use this skill to integrate Didit face-image age estimation, age-threshold checks, passive liveness review, and escalation paths for borderline age-verification cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes face images and age-estimation results, which can create privacy, consent, and legal-compliance risk.

Mitigation: Use it only with informed consent and legal authorization, and review the workflow before using it with real users.

Risk: API requests may retain face-image review data when save_api_request is enabled.

Mitigation: Consider setting save_api_request=false by default unless retention is required and approved.

Risk: Full API responses or vendor_data values may expose sensitive user information.

Mitigation: Avoid logging full responses, minimize vendor_data, and use a limited Didit API key in an isolated environment with pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rosasalberto/skills/didit-biometric-age-estimation)
- [Didit documentation](https://docs.didit.me)
- [Didit standalone age estimation API](https://docs.didit.me/standalone-apis/age-estimation)
- [Didit age estimation feature guide](https://docs.didit.me/core-technology/age-estimation/overview)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DIDIT_API_KEY and sends face images to the Didit age-estimation API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
