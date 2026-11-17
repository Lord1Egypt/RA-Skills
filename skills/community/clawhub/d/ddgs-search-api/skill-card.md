## Description:

Use when needing to search the web in AI coding tools or OpenClaw. Uses DuckDuckGo API without API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bird-frank](https://clawhub.ai/user/bird-frank)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to run DuckDuckGo web or news searches from the command line, with text or JSON output for automation. It supports result limits, region, safe search, time range, backend, and proxy options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation examples can lead users to run installer commands or install dependencies without pinning.

Mitigation: Review setup commands before use and prefer trusted, pinned, or lockfile-based installation of uv and ddgs.

Risk: Search queries and proxy URLs may expose secrets, credentials, private project names, or sensitive internal text to external services or proxies.

Mitigation: Avoid sending sensitive content in queries or proxy URLs, and use only trusted proxy endpoints.

Risk: The OpenClaw bash workflow example may be unsafe if a query is interpolated directly into a shell command.

Mitigation: Pass queries as command arguments or otherwise escape and validate them before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bird-frank/skills/ddgs-search-api)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON search results, with Markdown command examples and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search behavior is controlled by query, result limit, region, safe search, time limit, backend, news mode, JSON mode, verbosity, and proxy settings.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
