## Description:

Searches the web with DuckDuckGo and fetches URL content without requiring API keys, returning search results or extracted page content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengbin92](https://clawhub.ai/user/mengbin92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search the public web and retrieve readable content from public URLs when built-in web search is unavailable or an API-key-free search path is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetcher can request arbitrary URLs, including private-network, localhost, cloud metadata, or sensitive internal web applications if those destinations are reachable from the runtime.

Mitigation: Run the skill with outbound network restrictions and avoid using it to fetch untrusted or internal URLs.

Risk: The artifact instructs installation of an unused DuckDuckGo dependency, which may add unnecessary dependency exposure.

Mitigation: Remove the unused dependency guidance or pin and review any required package before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mengbin92/skills/duckduckgo-search-skill)
- [DuckDuckGo](https://duckduckgo.com)
- [Skill definition](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search or fetch results, with optional plain text fetch output and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include title, URL, and snippet. Fetch results include URL, title, extracted text, status code, and error metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
