## Description:

Use AgentRef's REST API from OpenClaw or any HTTP runtime for merchant onboarding, programs, affiliates, conversions, flags, and payouts; authenticate with AGENTREF_API_KEY, start with GET /api/v1/me, prefer safe reads, and confirm state-changing writes before sending them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukasvanuden](https://clawhub.ai/user/lukasvanuden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and operate AgentRef merchant REST workflows, including onboarding, program management, affiliate review, conversion checks, fraud flags, and payout records. It is intended for REST-first environments such as OpenClaw and requires an AgentRef API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform sensitive AgentRef merchant actions when a write-capable API key is available.

Mitigation: Use a dedicated least-privilege AGENTREF_API_KEY, start with read-only scopes for inspection, and grant write scopes only for confirmed changes.

Risk: State-changing operations can affect programs, affiliates, flags, onboarding, or payout records.

Mitigation: Inspect current state first, summarize the exact intended action, require user confirmation, and use Idempotency-Key on documented POST writes that support it.

Risk: An affiliate key cannot safely run merchant-admin workflows.

Mitigation: Start with GET /api/v1/me and restrict affiliate keys to explicitly requested affiliate self-service reads.

## Reference(s):

- [AgentRef ClawHub Skill Page](https://clawhub.ai/lukasvanuden/skills/agentref)
- [AgentRef Homepage](https://github.com/LukasvanUden/agentref)
- [AgentRef REST endpoints](references/endpoints.md)
- [AgentRef REST workflows](references/workflows.md)
- [AgentRef API base URL](https://www.agentref.co/api/v1)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, configuration]

**Output Format:** [Markdown guidance with HTTP endpoint references and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTREF_API_KEY; prompts for confirmation before state-changing writes.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
