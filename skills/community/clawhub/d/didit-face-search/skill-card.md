## Description:

Integrates Didit's Face Search API to search submitted face images against an application's enrolled faces for duplicate detection and blocklist screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Didit Face Search into backend applications for duplicate account detection and face blocklist screening. It provides API usage guidance and example code for submitting images and interpreting matches and warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face images and biometric match results are sent to an external face-search service, and saved requests enroll the submitted face by default.

Mitigation: Send images only when authorized, apply your privacy and retention requirements, and set save_api_request=false when saving and enrollment are not wanted.

Risk: The integration requires a Didit API key, and responses may contain match details and time-limited image URLs.

Mitigation: Keep DIDIT_API_KEY in a secret store, restrict its access, and limit retention and access to returned match data and image URLs.

Risk: Similarity matches can affect duplicate-account or blocklist decisions, while the API does not provide a liveness verdict.

Mitigation: Review match details and warnings before consequential decisions, and use a separate liveness check when liveness evidence is required.

## Reference(s):

- [Didit Face Search API Reference](https://docs.didit.me/standalone-apis/face-search)
- [Didit Face Search Feature Guide](https://docs.didit.me/core-technology/face-search/overview)
- [Didit Pricing](https://docs.didit.me/getting-started/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python and TypeScript examples, shell commands, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover API authentication, face search requests, and response handling.]

## Skill Version(s):

1.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
