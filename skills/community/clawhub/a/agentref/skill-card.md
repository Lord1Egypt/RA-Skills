## Description: <br>
Use AgentRef's REST API from OpenClaw or any HTTP runtime for merchant onboarding, programs, affiliates, conversions, flags, and payouts; authenticate with AGENTREF_API_KEY, start with GET /api/v1/me, prefer safe reads, and confirm state-changing writes before sending them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukasvanuden](https://clawhub.ai/user/lukasvanuden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect or operate AgentRef over REST for merchant onboarding, program management, affiliate review, conversion analysis, fraud flags, and payouts. It is intended for REST-first agent runtimes that can authenticate with AGENTREF_API_KEY and confirm state-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires AGENTREF_API_KEY, and misuse or exposure of that credential could allow access to AgentRef data or actions. <br>
Mitigation: Use a dedicated least-privilege key, prefer read-only scopes for inspection, and never print, log, echo, or persist the raw key. <br>
Risk: Write endpoints can change merchant onboarding, program settings, affiliate access, fraud flag resolution, or payout records. <br>
Mitigation: Inspect current state with GET requests first, summarize the exact intended write, require clear user confirmation, and send Idempotency-Key where the endpoint supports it. <br>
Risk: Using an affiliate key for merchant-admin workflows could lead to incorrect or unauthorized workflow attempts. <br>
Mitigation: Start with GET /api/v1/me, check ownerType, and restrict affiliate keys to affiliate self-service reads unless the user explicitly changes scope. <br>


## Reference(s): <br>
- [AgentRef homepage](https://github.com/LukasvanUden/agentref) <br>
- [AgentRef REST endpoints](references/endpoints.md) <br>
- [AgentRef REST workflows](references/workflows.md) <br>
- [ClawHub AgentRef skill page](https://clawhub.ai/lukasvanuden/agentref) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with HTTP endpoint paths, JSON request details, and response handling notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTREF_API_KEY; API responses follow data/meta or error/meta envelopes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
