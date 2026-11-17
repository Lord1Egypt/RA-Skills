## Description:

Read angi.com (US home-services directory) from a shell with the fpx CLI (@fetchproxy/cli) instead of running the angi-mcp server — find pros by trade and city, read a pro's profile, ratings breakdown and reviews, and list the trade/city taxonomy. Use when you want Angi data without the MCP, in a script, or on a machine where the MCP isn't installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and home-services researchers can use this skill to look up Angi professionals by trade and city, inspect profiles and reviews, and list available trade and city combinations. Public listings use an open Angi tab; private account lookups are optional and use the signed-in user's own account.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The external fpx CLI and ContextMint Bridge extension are outside this package, and their code is not verified by the security assessment.

Mitigation: Review the CLI and extension before installing them.

Risk: Browser pairing persists, and account lookups expose retrieved private account information to the agent.

Mitigation: Keep access scoped to angi.com; pair my.angi.com only when private account lookups are needed, and request only the account information required.

## Reference(s):

- [Angi page shapes and extraction recipes](references/angi-pages.md)
- [Bundled Angi page data extractor](references/rsc.mjs)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [Angi trade sitemap](https://www.angi.com/sitemap/statecat-sitemap.xml)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text or JSON results with shell commands and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results may include public business profiles, ratings, reviews, and taxonomy; signed-in account data is optional.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
