## Description:

Helps developers integrate Didit's selfie-based age-estimation and passive liveness API into age-gating workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write backend integrations for Didit's age-estimation API, configure age and liveness thresholds, and handle results in age-gating flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A selfie and related age-estimation data are sent to an external verification service, and requests may be saved by default.

Mitigation: Tell users how their image will be handled before collection, and set save_api_request=false when session storage and face-search indexing are not needed.

Risk: An exposed API key could allow unauthorized verification requests.

Mitigation: Keep DIDIT_API_KEY in server-side secret storage and do not expose it in client code.

Risk: A face-based age estimate is approximate and is not proof of legal age, especially near a cutoff.

Mitigation: Use the estimate as a low-friction check and route borderline cases to document verification.

## Reference(s):

- [Didit Age Estimation API Reference](https://docs.didit.me/standalone-apis/age-estimation)
- [Didit Age Estimation Feature Guide](https://docs.didit.me/core-technology/age-estimation/overview)

## Skill Output:

**Output Type(s):** [Code, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes request and response handling guidance.]

## Skill Version(s):

1.3.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
