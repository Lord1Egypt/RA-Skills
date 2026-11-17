## Description:

Sell a custom OpenAI-compatible endpoint on the asale market by probing it, connecting it as an account, and setting seller terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect a custom OpenAI-compatible API endpoint to a local asale daemon, review sellable models, set pricing and concurrency terms, and publish the endpoint on the asale market.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and update path runs code from a live asale.ai download URL.

Mitigation: Review before installing; only run the installer if the user trusts the live download path, or prefer a pinned or signed release when available.

Risk: Connecting a custom endpoint probes with the supplied API key and stores that key in the daemon.

Mitigation: Confirm the exact base URL and key before connecting, and prefer a revocable, scoped API key.

Risk: A low price floor on a metered endpoint can sell traffic below the user's own token cost.

Mitigation: Calculate the endpoint's real token cost before setting minRatio, and review concurrency and daily-token limits before enabling selling.

Risk: Selling requires a local daemon token and an authenticated asale session.

Mitigation: Keep the daemon token private, use loopback for RPC calls, and stop on sign-in errors instead of attempting alternate routes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/asale-sell-endpoint)
- [asale homepage](https://asale.ai)
- [asale source repository](https://github.com/asale-ai/asale)
- [Publisher profile](https://clawhub.ai/user/dlazyai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local daemon RPC calls and explains status, pricing, authentication, and error-handling outcomes.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
