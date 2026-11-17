## Description:

Diagnoses OpenClaw configuration and runtime state, including output validation, backend model health, knowledge graph status, memory source attribution, degradation notices, and long-conversation truncation behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelfeng](https://clawhub.ai/user/michaelfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw or ClawBrain configuration, model backend health, knowledge graph state, and memory-related behavior. It provides diagnostic guidance and authenticated curl checks for relevant service endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnostic curl checks send authenticated requests to api.factorhub.cn.

Mitigation: Verify that api.factorhub.cn is the intended trusted service endpoint before running the checks.

Risk: Bearer tokens used for diagnostics could expose broader account access if copied from a high-privilege credential.

Mitigation: Use a scoped token for diagnostics instead of a broad account credential.

## Reference(s):

- [ClawBrain Dashboard](https://clawbrain.dev/dashboard)
- [Backend health endpoint](https://api.factorhub.cn/v1/health/backends)
- [Knowledge graph stats endpoint](https://api.factorhub.cn/v1/graph/stats)
- [Model list endpoint](https://api.factorhub.cn/v1/models)
- [ClawHub skill page](https://clawhub.ai/michaelfeng/skills/clawbrain-pro-doctor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands that require a trusted endpoint and scoped bearer token.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
