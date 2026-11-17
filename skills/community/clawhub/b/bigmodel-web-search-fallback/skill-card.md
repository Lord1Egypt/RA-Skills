## Description:

Use Zhipu / BigModel web search as a fallback when the built-in web_search route is unavailable, with raw structured results or chat-completions search summaries across supported search engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxhdky2345](https://clawhub.ai/user/gxhdky2345)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when built-in web search is unavailable or when a user specifically requests Zhipu, BigModel, or GLM search. It helps choose a search engine, run the wrapper script, and return either structured results for agent synthesis or a chat-generated search summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and optional request_id or user_id values are sent to BigModel/Zhipu.

Mitigation: Use only where that provider use is approved, and avoid secrets, personal data, or confidential internal content.

Risk: Chat mode returns a synthesized answer that may need validation before use.

Mitigation: Sanity-check synthesized answers and review source links before presenting final claims.

Risk: The wrapper requires API-key environment variables and external network access.

Mitigation: Confirm the runtime is authorized for BigModel/Zhipu API access, and stop when credentials are missing.

## Reference(s):

- [Zhipu Web Search Notes](references/api-notes.md)
- [BigModel Web Search API endpoint](https://open.bigmodel.cn/api/paas/v4/web_search)
- [BigModel Chat Completions API endpoint](https://open.bigmodel.cn/api/paas/v4/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and JSON command output from the wrapper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script can emit structured JSON search results or a synthesized chat answer, depending on mode.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
