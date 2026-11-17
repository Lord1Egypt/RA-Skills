## Description:

Researches and analyzes content across decentralized social networks (Farcaster, Lens, Nostr, and Bluesky) using the deso-ag CLI tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtple](https://clawhub.ai/user/mtple)

### License/Terms of Use:


## Use Case:

Developers, researchers, and analysts use this skill to search decentralized social networks, inspect trending posts, extract discussion terms, browse Farcaster channels, and synthesize findings for users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs the external deso-ag npm package.

Mitigation: Review the package and version before global installation, and install only if you trust it.

Risk: Optional Farcaster and Bluesky credentials may be exposed if broad environment secrets are available during execution.

Mitigation: Use scoped or revocable credentials and avoid exposing unrelated environment secrets when running deso-ag.

Risk: Network coverage may be incomplete when API keys are missing, APIs are rate limited, or Nostr is slow or inconsistent.

Mitigation: Tell users which networks were included, retry transient Nostr failures once, and explain missing or rate-limited results.

## Reference(s):

- [deso-ag Command Reference](references/command-reference (1).md)
- [deso-ag npm package](https://www.npmjs.com/package/deso-ag)
- [ClawHub skill page](https://clawhub.ai/mtple/skills/deso-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash commands and structured JSON-derived summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses compact JSON results from deso-ag for synthesis and may include source post links.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
