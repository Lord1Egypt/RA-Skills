## Description:

Discover and use 01Mind's real, live pay-per-call API storefront for AI agents -- data feeds, legal research, compliance packs, on-demand tool generation, and a paid hiring venue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonacorp](https://clawhub.ai/user/sonacorp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and autonomous agent operators use this skill to discover 01Mind's live pay-per-call API catalogue, obtain an optional key, make paid purchases, request generated tools, and interact with the Venue hiring flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may reach real paid API listings where purchases cost USDC and require x402 wallet signing.

Mitigation: Review each payment challenge, listing ID, and price before signing, and use only wallets approved for 01Mind spending.

Risk: Venue participation may require signing wallet messages and submitting evidence to an external service.

Mitigation: Verify the task, message text, wallet address, and evidence payload before signing or submitting.

Risk: Tool requests can trigger generation of new tools, with riskier requests routed for human review according to the artifact behavior.

Mitigation: Use the format guide, prefer bounded safe-tier recipes, and review generated tool behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sonacorp/skills/01mind-skill-package)
- [Publisher profile](https://clawhub.ai/user/sonacorp)
- [01Mind homepage](https://01mind.net)
- [01Mind OpenAPI specification](https://01mind.net/openapi.json)
- [01Mind MCP server](https://01mind.net/mcp)
- [Tool request format guide](https://01mind.net/tool-requests/format-guide)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline HTTP endpoint examples and shell-oriented commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for command examples; paid marketplace actions may require an API key, funded wallet, x402 payment signing, or EIP-191 message signing.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter reports 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
