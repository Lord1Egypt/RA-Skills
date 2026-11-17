## Description:

AI-powered code review with intelligent model routing that returns structured findings while optimizing model cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beee003](https://clawhub.ai/user/beee003)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to review diffs, pull requests, or individual files for bugs, security issues, style concerns, and suggested fixes. It supports standard, strict, and security-focused review modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed code, diffs, and optional provider API keys can be sent to Astrai and routed to third-party model providers.

Mitigation: Use tightly scoped Astrai and provider keys, start with non-sensitive repositories, and confirm the credential disclosure model before enabling BYOK routing.

Risk: A configurable ASTRAI_BASE_URL can redirect code and credentials to a different endpoint.

Mitigation: Do not set ASTRAI_BASE_URL unless the destination is fully trusted, and avoid running the skill in environments that contain unrelated LLM provider keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beee003/skills/astrai-code-review)
- [Astrai homepage](https://as-trai.com)
- [Astrai chat completions endpoint](https://as-trai.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Structured JSON review results with issue lists, severity, summary text, model used, cost, and savings fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ASTRAI_API_KEY; optional provider keys enable BYOK routing; REVIEW_STRICTNESS controls standard, strict, or security review mode.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
