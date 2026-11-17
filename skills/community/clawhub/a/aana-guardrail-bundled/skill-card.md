## Description:

Provides guardrail instructions and a bundled Python helper that sends minimal, redacted review payloads to a trusted localhost AANA HTTP bridge for policy guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a local guardrail review step before taking actions that need policy guidance. The helper packages a minimal review payload, posts it to a user-approved localhost AANA bridge, and treats non-accept recommendations as prompts to revise, ask, defer, or refuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payloads may contain sensitive or unnecessary private information if prepared carelessly.

Mitigation: Use redacted summaries only, omit secrets and full private records, and delete temporary payload files unless an audit record is explicitly required.

Risk: The helper depends on the trustworthiness of the configured local AANA bridge.

Mitigation: Run it only with a reviewed localhost bridge approved by the user or administrator; use manual review when no trusted bridge is available.

Risk: Strict localhost-only deployments may be exposed to redirect behavior from the HTTP client stack.

Mitigation: Prefer a helper version that rejects redirects when strict localhost-only networking is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-guardrail-bundled)
- [Publisher profile](https://clawhub.ai/user/mindbomber)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Package manifest](artifact/manifest.json)
- [Review payload schema](artifact/schemas/review-payload.schema.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown instructions with JSON payload examples and helper JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local payload file and a trusted localhost AANA bridge; exits nonzero when the recommendation is not accept.]

## Skill Version(s):

1.0.1 (source: server release evidence, created 2026-05-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
