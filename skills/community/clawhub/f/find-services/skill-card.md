## Description:

Finds and shortlists third-party service providers for an agent capability using OpenSpend CLI marketplace search, limited to discovery and recommendation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albertpurnama](https://clawhub.ai/user/albertpurnama)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to discover and compare external service providers for a requested capability. It returns a concise shortlist and usage guidance while keeping installation, authentication setup, credential handling, payments, and purchases out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace discovery may require an existing OpenSpend session or a login prompt.

Mitigation: Use an existing CLI session when available, and require explicit user confirmation before running any authentication command.

Risk: Service discovery can lead to paid calls, payment setup, or provider onboarding decisions.

Mitigation: Keep this skill limited to discovery; request explicit user approval and hand off payment or setup work to a separate flow before any paid action.

Risk: A listed service may not meet the user's reliability, security, or capability requirements in practice.

Mitigation: Start with a small validation call, capture request and response examples, and define success criteria before scaling usage.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown service shortlist with concise rationale, optional command snippets, and a recommended usage note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 5 services in marketplace order and avoids additional ranking commentary.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
