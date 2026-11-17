## Description:

Verify any Brazilian company (CNPJ) with official data: registry status, partners, sanctions, bank licence, contracts, funds. Pay per call via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aladaf](https://clawhub.ai/user/aladaf)

### License/Terms of Use:

MIT-0

## Use Case:

External users, compliance teams, procurement teams, and agents use this skill to check Brazilian companies by CNPJ for onboarding, KYB review, sanctions screening, licensing checks, public contracts, and fund verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries disclose the submitted Brazilian company identifier or name to api.brazilayer.com.

Mitigation: Use the skill only for intended KYB checks and avoid submitting sensitive queries unless disclosure to the service is acceptable.

Risk: Paid routes can spend small amounts of USDC through x402 or agentcash.

Mitigation: Validate CNPJ check digits with the free route first and confirm paid calls when the query or relationship is sensitive.

Risk: Paid routes may request payment before validating whether a CNPJ exists.

Mitigation: Run the free check-digit validation before paid lookups and start with the lowest-cost status route unless the user clearly needs a broader profile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aladaf/skills/brazil-kyb)
- [Brazilayer API documentation](https://api.brazilayer.com/docs)
- [Brazilayer x402 route metadata](https://api.brazilayer.com/.well-known/x402)
- [Brazilayer service ratings](https://agenteconomy.report/s/api.brazilayer.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API calls]

**Output Format:** [Markdown with inline API routes and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include Portuguese legal field names translated or explained for the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
