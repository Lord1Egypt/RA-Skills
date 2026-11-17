## Description:

AgentClear enables agents to discover APIs in natural language, proxy calls to paid services, list marketplace services, and check account or balance status through an AgentClear API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwflickinger](https://clawhub.ai/user/dwflickinger)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an OpenClaw agent discover paid API services, evaluate pricing and trust metadata, call selected services through AgentClear, and inspect marketplace or account status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may send user payloads to dynamically selected paid third-party services.

Mitigation: Require manual confirmation before each proxy request and review the payload, selected provider, and price before allowing the call.

Risk: AgentClear API key use can incur paid per-call charges.

Mitigation: Use a scoped, revocable API key and configure account-level spending limits where available.

Risk: Mutable main-branch install commands may change after review.

Mitigation: Install from a pinned reviewed commit or verified release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dwflickinger/skills/agentclear)
- [AgentClear](https://agentclear.dev)
- [AgentClear API Docs](https://agentclear.dev/docs)
- [AgentClear Security](https://agentclear.dev/security)
- [AgentClear Bounty Board](https://agentclear.dev/bounties)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTCLEAR_API_KEY and can cause paid per-call API usage through selected AgentClear services.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
