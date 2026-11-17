## Description:

Autoglm Websearch uses the AutoGLM Web Search API to retrieve current web information, page snippets, and source links for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyfujian](https://clawhub.ai/user/flyfujian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill when an agent needs live web search results, current information, or retrieved web page snippets with cited sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and a locally obtained bearer token are sent to AutoGLM.

Mitigation: Avoid using the skill for secrets, private internal identifiers, or sensitive prompts.

Risk: The security evidence reports an exposed API signing secret in the bundled script.

Mitigation: Review the skill before installing and prefer a version that removes the bundled signing key and declares narrower network and token permissions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/flyfujian/skills/autoglm-websearch)
- [AutoGLM Web Search API endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/web-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown summary with reference links; the bundled script prints formatted JSON from the API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to AutoGLM and a bearer token from the local token service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
