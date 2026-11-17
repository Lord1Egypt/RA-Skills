## Description:

Host-side AffixIO attestation before high-value agent actions; signed allow/deny without sending PII off-host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[affixio](https://clawhub.ai/user/affixio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use AffixIO to add signed allow/deny attestation gates before privileged or irreversible agent actions such as payments, destructive operations, outbound sends, and tool execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for high-value action gates and relies on external AffixIO packages and project trust.

Mitigation: Verify that the AffixIO npm packages and GitHub project are trusted before installing or enabling the skill.

Risk: Attestation prompts could expose sensitive data if raw credentials, secrets, or PII are included.

Mitigation: Keep tool arguments hashed or summarized, and do not paste secrets or PII into AffixIO prompts.

Risk: Privileged actions may proceed without the intended control if attestation is performed after execution or verification is skipped.

Mitigation: Attest before the high-value tool runs, and fail closed on deny or verification failure.

## Reference(s):

- [AffixIO skill on ClawHub](https://clawhub.ai/affixio/skills/affixio)
- [AffixIO MCP](https://github.com/AffixIO/affixio-mcp)
- [AffixIO SDK](https://github.com/AffixIO/SDK)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and AFFIX_API_KEY for the documented MCP path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
