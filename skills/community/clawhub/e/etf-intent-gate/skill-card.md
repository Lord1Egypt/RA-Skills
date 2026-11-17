## Description:

Classifies and filters ETF research queries before multi-agent dispatch, rewriting allowed requests into structured research tasks and intercepting unsupported, unsafe, or unclear inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nothingstop](https://clawhub.ai/user/nothingstop)

### License/Terms of Use:

MIT

## Use Case:

Developers and platform teams use this skill as a gateway in ETF, industry, or index research systems to classify user intent, apply safety guardrails, rewrite allowed queries, and decide whether to forward work to downstream research agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports raw user query exposure in scheduler payloads and recommends review before installation.

Mitigation: Remove original_user_query from scheduler payloads, avoid logging raw prompts, and pass only rewritten or sanitized task text to downstream agents.

Risk: The security review reports fail-open and configuration risks.

Mitigation: Use the conservative degradation mode for financial workflows and require deployment review before enabling loose pass-through behavior.

Risk: The security review recommends restricting the LLM base URL.

Mitigation: Allow only approved HTTPS LLM providers for INTENT_LLM_BASE_URL and keep API keys in managed secrets rather than source files.

Risk: The security review recommends pinned dependencies or a lockfile.

Mitigation: Pin runtime dependencies or add a reviewed lockfile before production deployment.

## Reference(s):

- [ETF intent gate design](artifact/references/design.md)
- [ClawHub skill page](https://clawhub.ai/nothingstop/skills/etf-intent-gate)

## Skill Output:

**Output Type(s):** [text, JSON, guidance, configuration]

**Output Format:** [JSON task context for forwarded requests, or a direct text response for intercepted and platform-QA requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires INTENT_LLM_API_KEY and INTENT_LLM_BASE_URL for live LLM calls; without an API key, the artifact documents a local mock mode.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
