## Description:

Verify external factual claims in draft content before publishing or sending, and produce a structured claim verification report with evidence links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jernejcicorbin-hub](https://clawhub.ai/user/jernejcicorbin-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, marketers, and publishing teams use this skill to check factual claims in drafts before publication or sending. It helps identify wrong, weak, conflicting, or unsupported claims and can produce a structured JSON report when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft claim text and the Prismfy API key may be sent to Prismfy or another configured endpoint.

Mitigation: Use the skill only with trusted endpoints and approved draft content, keep PRISMFY_BASE_URL unset unless the alternate endpoint is explicitly trusted, and scope the API key appropriately.

Risk: The setup guidance suggests persisting PRISMFY_API_KEY in ~/.bashrc.

Mitigation: Store the API key in a safer secret store or session-scoped environment instead of a long-lived shell startup file.

Risk: The bootstrap hook can add persistent reminders in future agent sessions.

Mitigation: Enable the hook only when ongoing claim-verification reminders are desired, and review hook behavior before installing it into the hooks registry.

Risk: The batch helper uses preliminary heuristics and may return weak or not_found results that still require judgment.

Mitigation: Require human review of evidence before publishing and keep claims non-verified unless supporting evidence meets the skill's stated source policy.

## Reference(s):

- [Pre-Publish Fact Checker on ClawHub](https://clawhub.ai/jernejcicorbin-hub/skills/claim-verifier)
- [Publisher profile](https://clawhub.ai/user/jernejcicorbin-hub)
- [Prismfy](https://prismfy.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Concise Markdown summary in chat, optional claim_verification_report.json artifact, and shell command examples for Prismfy-backed checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report items include claim, status, confidence, evidence_urls, failure_code, and notes; statuses are verified, weak, conflicting, or not_found.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
