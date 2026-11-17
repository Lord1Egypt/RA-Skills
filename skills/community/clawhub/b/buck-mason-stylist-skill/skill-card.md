## Description:

Personal shopping skill for Buck Mason that supports stock checks, wardrobe gap analysis, season- and event-aware outfit suggestions, AI try-on lookbooks, and one-shot MPP checkout via link-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickmerwin](https://clawhub.ai/user/nickmerwin)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping agents use this skill to check Buck Mason inventory, create personalized outfit and lookbook recommendations, manage order tracking or returns, and run explicitly confirmed agent-driven checkout flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public-by-link hosted lookbooks can expose styling choices, generated imagery, and feedback links to anyone with the URL.

Mitigation: Confirm before public deployment, use private hosting where available, and avoid sharing sensitive customer details in generated lookbook content.

Risk: Default voting endpoints may collect partner or stakeholder feedback without authentication.

Mitigation: Use --no-voting for read-only lookbooks or add authentication before collecting private feedback.

Risk: Shopping and account state may persist locally, including wishlist, purchase, or token-related data.

Mitigation: Prefer order-code flows over saved JWTs, avoid storing payment credentials, and review local files before shared or managed deployments.

Risk: Untrusted lookbook configuration or picks JSON can affect generated files and hosted output.

Mitigation: Run builders only on trusted inputs and validate generated lookbooks before sharing or deploying.

Risk: Checkout, returns, email access, and public deployment can have financial, privacy, or account consequences.

Mitigation: Require explicit same-turn confirmation before payment, return initiation, mailbox access, or public publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickmerwin/skills/buck-mason-stylist-skill)
- [Pima MCP API reference](references/mcp-api.md)
- [Pima order and returns API reference](docs/advanced/pima-api.md)
- [Image generation reference](references/image-generation.md)
- [Lookbook output formats](references/output-formats.md)
- [MPP checkout reference](references/mpp.md)
- [Voting reference](references/voting.md)
- [OpenAI API keys](https://platform.openai.com/api-keys)
- [OpenAI gpt-image-2 verification](https://help.openai.com/en/articles/10910291)
- [Stripe link-cli source](https://github.com/stripe/link-cli)
- [Stripe link-cli npm package](https://www.npmjs.com/package/@stripe/link-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with compact tables, product links, shell commands, configuration snippets, and optional generated lookbook files such as PNG, PPTX, or hosted HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external commerce, image-generation, hosting, voting, and payment-token services when the relevant workflow and user confirmation require them.]

## Skill Version(s):

0.7.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
