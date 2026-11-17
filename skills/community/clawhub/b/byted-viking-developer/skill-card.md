## Description:

Guides developers through Viking SDK integration, covering VikingDB, KnowledgeBase, and Memory setup, authentication, API calls, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill with Trae, OpenCode, Codex, Claude Code, or Antigravity to integrate Viking SDKs for vector search, knowledge-base workflows, long-term memory, and SDK/API issue diagnosis. The skill evidence states that OpenClaw scenarios are not supported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some referenced examples show sensitive Viking memory/API traffic over unencrypted HTTP.

Mitigation: Use HTTPS for authenticated SDK and API calls, and do not copy HTTP examples into real environments.

Risk: SDK examples use AK/SK or API keys and include update/delete operations that can modify or remove data.

Mitigation: Use least-privilege credentials, keep secrets in environment or secret-management systems, and review delete/update calls against non-production data first.

Risk: The skill states that OpenClaw scenarios are not supported.

Mitigation: Use the skill only in the supported agent environments named by the release evidence.

Risk: Dependency versions in SDK examples may change over time.

Mitigation: Pin dependency versions and validate examples against the current Viking SDK documentation before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-viking-developer)
- [VikingDB Python SDK guide](resources/vikingdb-python-sdk.md)
- [VikingDB Go SDK guide](resources/vikingdb-go-sdk.md)
- [VikingDB Java SDK guide](resources/vikingdb-java-sdk.md)
- [KnowledgeBase Python SDK guide](resources/knowledge-python-sdk.md)
- [KnowledgeBase Go SDK guide](resources/knowledge-go-sdk.md)
- [Memory Python SDK guide](resources/memory-python-sdk.md)
- [VolcEngine VikingDB documentation](https://www.volcengine.com/docs/84313/1339026)
- [VolcEngine related SDK documentation](https://www.volcengine.com/docs/84313/1606319?lang=zh#1ab381b9)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code snippets, SDK call examples, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated API examples and destructive update/delete examples that require user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
