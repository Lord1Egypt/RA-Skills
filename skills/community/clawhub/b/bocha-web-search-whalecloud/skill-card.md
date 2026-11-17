## Description:

Provides Chinese web search and AI search through the Bocha API proxied by Whalecloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littlewangupup](https://clawhub.ai/user/littlewangupup)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Chinese web sources, verify current facts, cite sources, and request AI-summarized answers for news, policy, finance, company, product, and person information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Whalecloud's Bocha proxy.

Mitigation: Avoid searches containing secrets, credentials, or sensitive personal data.

Risk: The skill requires WHALECLOUD_API_KEY in its environment.

Mitigation: Store the token only in the configured skill environment and do not display, log, or share it.

Risk: Broad activation could send unnecessary external searches.

Mitigation: Use tighter activation rules when external search should be limited.

## Reference(s):

- [Bocha API detailed specification](references/api-spec.md)
- [Whalecloud Bocha API proxy](https://lab.iwhalecloud.com/gpt-proxy/bocha/v1/)
- [ClawHub skill page](https://clawhub.ai/littlewangupup/skills/bocha-web-search-whalecloud)
- [Publisher profile](https://clawhub.ai/user/littlewangupup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON search results and source references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WHALECLOUD_API_KEY and sends search queries to Whalecloud's Bocha proxy.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
