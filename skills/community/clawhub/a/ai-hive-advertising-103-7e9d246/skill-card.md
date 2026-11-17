## Description:

This skill guides Chinese-language AI-HIVE advertising workflows for luxury scarf pattern and equestrian graphic concepts, covering planning, rights checks, model routing, sample generation, task tracking, and delivery review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand marketers, ecommerce merchants, advertising agencies, retail teams, and content marketing teams use this skill to plan and produce AI-HIVE image and video advertising assets from verified product claims, audience needs, and channel constraints. It emphasizes original concepts, rights tracking, budget confirmation, task recovery, and acceptance checks before paid generation or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script may send API credentials to an endpoint selected through AI_HIVE_MCP_URL.

Mitigation: Before using API credentials, keep AI_HIVE_MCP_URL unset or verify that it exactly matches the official AI-HIVE MCP endpoint.

Risk: Paid generation, batch actions, sending, or public publishing may create cost or release risk.

Mitigation: Review current model prices and obtain explicit user approval before each paid, batch, send, or public publish action.

Risk: The activation scope is broad enough to require review before installation.

Mitigation: Install only when this Chinese-language AI-HIVE advertising workflow is intended, and review the skill before deployment.

Risk: API keys or OAuth tokens could be exposed through prompts, logs, screenshots, or repository files.

Mitigation: Prefer OAuth through the MCP client or store API keys only in trusted secret storage; never paste credentials into skill text, prompts, logs, screenshots, or code.

## Reference(s):

- [Original AI-HIVE Workflow](references/original-workflow.md)
- [AI-HIVE MCP Login and Binding Guide](references/mcp-binding.md)
- [AI-HIVE OAuth MCP Configuration Example](references/mcp-config.example.json)
- [AI-HIVE API Key MCP Configuration Example](references/mcp-config-api-key.example.json)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-103-7e9d246)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local work-order JSON and AI-HIVE task records when the user confirms the workflow steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
