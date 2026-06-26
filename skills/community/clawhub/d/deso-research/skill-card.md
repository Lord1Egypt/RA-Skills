## Description: <br>
Research and analyze content across decentralized social networks (Farcaster, Lens, Nostr, Bluesky) using the deso-ag CLI tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtple](https://clawhub.ai/user/mtple) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to query decentralized social networks with deso-ag and synthesize trends, topics, high-engagement posts, and cross-network comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on installing and running the third-party deso-ag npm package. <br>
Mitigation: Install it only when the package is trusted, and use an isolated environment when extra caution is needed. <br>
Risk: Optional API keys and Bluesky app-password credentials may be used for fuller network coverage. <br>
Mitigation: Provide only the credentials needed for the requested networks and avoid including secrets in prompts or searches. <br>
Risk: Search terms may be sent to external decentralized social-network services. <br>
Mitigation: Avoid sensitive personal details in queries and tell users which networks are being queried based on available credentials. <br>


## Reference(s): <br>
- [deso-ag npm package](https://www.npmjs.com/package/deso-ag) <br>
- [deso-ag Command Reference](references/command-reference (1).md) <br>
- [ClawHub skill page](https://clawhub.ai/mtple/deso-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown summaries with source links, supported by deso-ag shell commands and compact JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and trending workflows use compact JSON for agent analysis; term extraction uses JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
