## Description:

Web search via self-hosted SearxNG. Aggregates Google, Bing, DuckDuckGo, Brave. Returns title/url/snippet. Zero API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sexychina](https://clawhub.ai/user/sexychina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Ask Search to query a local or trusted SearxNG instance and receive search result titles, URLs, snippets, or raw JSON for follow-up browsing and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and setup guidance may create local installation risk, especially when writing to system paths or using temporary files.

Mitigation: Review before installing, prefer a user-writable bin directory, and avoid elevated installation unless the installer behavior has been reviewed.

Risk: Search and deep-fetch workflows can expose queries, credentials, or browsing context if SEARXNG_URL, proxy tunnels, or logged-in browser sessions are not trusted.

Mitigation: Keep SEARXNG_URL local or trusted, pin dependencies, and avoid persistent proxy or logged-in browser workflows unless their privacy and policy implications are understood.

## Reference(s):

- [Ask Search on ClawHub](https://clawhub.ai/sexychina/skills/ask-search)
- [SearxNG](https://github.com/searxng/searxng)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, JSON, URLs, shell commands, configuration]

**Output Format:** [CLI text result list, newline-delimited URLs, or JSON search result objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local or trusted SearxNG endpoint; MCP search limits requested results to a maximum of 20.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
