## Description: <br>
Personal shopping skill for Buck Mason. Stock-checks (online + nearby store), wardrobe gap analysis, season- and event-aware outfit suggestions, AI try-on lookbooks, and one-shot MPP checkout via link-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickmerwin](https://clawhub.ai/user/nickmerwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Buck Mason shoppers and their agents use this skill to check live stock, build outfit recommendations from profile, wardrobe, and event context, generate try-on or editorial lookbooks, and optionally complete MPP checkout after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global, subject to Buck Mason storefront, payment, shipping, and local data-transfer availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use personal profile data, including sizes, zip codes, photos, and contact or shipping details for selected workflows. <br>
Mitigation: Keep profile.md minimal and provide shipping details or photos only for workflows that require them. <br>
Risk: The skill can generate and publish try-on lookbooks that may expose personal imagery or partner vote data. <br>
Mitigation: Use local-only output or --no-voting for private lookbooks, and only enable auto-publishing when the chosen host's privacy posture is acceptable. <br>
Risk: The optional MPP checkout path can complete purchases through @stripe/link-cli. <br>
Mitigation: Leave @stripe/link-cli uninstalled unless agent-driven checkout is desired, and require explicit item, total, shipping, and return-policy confirmation before payment. <br>
Risk: Account-wide order history may involve tokens or email magic links. <br>
Mitigation: Prefer guest order-code lookup, avoid saving JWTs, and require explicit authorization before any email MCP retrieval. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/nickmerwin/buck-mason-stylist-skill) <br>
- [Pima MCP API reference](references/mcp-api.md) <br>
- [Merchant Payments Protocol reference](references/mpp.md) <br>
- [Image generation workflow](references/image-generation.md) <br>
- [Lookbook output formats](references/output-formats.md) <br>
- [Voting capability reference](references/voting.md) <br>
- [OpenAI API keys](https://platform.openai.com/api-keys) <br>
- [gpt-image-2 verification guidance](https://help.openai.com/en/articles/10910291) <br>
- [Stripe link-cli source](https://github.com/stripe/link-cli) <br>
- [Stripe link-cli package](https://www.npmjs.com/package/@stripe/link-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with structured API examples, shell commands, configuration snippets, generated files, and hosted lookbook artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local lookbook files, hosted lookbook URLs, product recommendations, stock summaries, checkout handoff details, and validation summaries depending on the workflow.] <br>

## Skill Version(s): <br>
0.7.2 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
