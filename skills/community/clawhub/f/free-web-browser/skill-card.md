## Description:

Browse web through OpenClaw web_search and web_fetch with Ollama as search provider, no external API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prantikmedhi](https://clawhub.ai/user/prantikmedhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search the live web, fetch source pages, compare evidence, and summarize current information using configured OpenClaw web_search and web_fetch tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and fetched URLs or page content may be sent to the configured web provider.

Mitigation: Avoid private or sensitive topics unless the configured OpenClaw web provider setup is acceptable.

Risk: Live web results can be stale, incomplete, blocked, or inconsistent across sources.

Mitigation: Prefer primary sources, fetch pages before relying on claims, cross-check important facts, and include recency or uncertainty notes.

Risk: The skill cannot browse live web if the runtime does not expose web_search and web_fetch.

Mitigation: Verify tool availability and provider configuration before relying on the skill for current information.

## Reference(s):

- [Ollama Web Browser Notes](references/ollama-web-browser-notes.md)
- [ClawHub skill page](https://clawhub.ai/prantikmedhi/skills/free-web-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown answer with source links and brief uncertainty notes when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise evidence bullets, caveats, and source URLs.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
