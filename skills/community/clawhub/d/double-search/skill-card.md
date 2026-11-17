## Description:

双搜索功能 (Tavily + Kimi) - 支持并行搜索和结果合并

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjs028-coder](https://clawhub.ai/user/wjs028-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run a search query through Tavily and Kimi, then receive merged or source-separated results for research, content preparation, technical lookup, or market analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Tavily and, when configured, Moonshot/Kimi.

Mitigation: Avoid submitting secrets, private customer data, or confidential business text as search queries.

Risk: The installer prints partial API key prefixes while checking configuration.

Mitigation: Run installation only in controlled terminals and avoid shared logs or recorded sessions when credentials are present.

Risk: Runtime behavior depends on external API availability, credentials, and response formats.

Mitigation: Validate provider credentials and result parsing in the deployment environment before relying on the skill for production workflows.

Risk: The installer installs Python dependencies without pinned versions.

Mitigation: Pin and review aiohttp and python-dotenv versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjs028-coder/skills/double-search)
- [Tavily API dashboard](https://app.tavily.com/)
- [Moonshot/Kimi API](https://api.moonshot.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON-like Python dictionaries, text logs, and Markdown documentation with inline Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include query text, merged result items, and per-source result breakdowns when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
