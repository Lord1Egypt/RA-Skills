## Description:

Custom Grok Search lets an agent use xAI-compatible Responses API search tools for web search, X/Twitter search, text chat, image chat, model listing, and lightweight self-tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangjiongjie](https://clawhub.ai/user/zhangjiongjie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to route web and X/Twitter research, Grok-compatible chat, image prompts, and model discovery through official xAI endpoints or trusted compatible proxies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace-controlled environment files can redirect API calls to a third-party Grok-compatible endpoint while user-level API credentials are available.

Mitigation: Install only in trusted workspaces, prefer official xAI endpoints, and do not let untrusted projects supply .env values such as XAI_BASE_URL or CUSTOM_GROK_BASE_URL.

Risk: Sensitive prompts or images may be sent to a configured third-party proxy.

Mitigation: Avoid sending sensitive prompts or images through third-party proxies; use explicitly trusted endpoints and keys.

## Reference(s):

- [Configuration Reference](references/config.md)
- [xAI Tools Quick Links](references/xai-tools-links.md)
- [xAI Search Tools Guide](https://docs.x.ai/docs/guides/tools/search-tools)
- [xAI Tools Overview](https://docs.x.ai/docs/guides/tools/overview)
- [xAI API Reference](https://docs.x.ai/docs/api-reference)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON search result objects, plain text answers, link lists, and Markdown guidance with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results can include titles, URLs, snippets, authors, timestamps, and citations; chat supports optional local image inputs for JPEG, PNG, WEBP, and GIF files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
