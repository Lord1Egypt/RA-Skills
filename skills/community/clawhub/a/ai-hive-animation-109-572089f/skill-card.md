## Description:

This Chinese-language AI-HIVE workflow helps animation, comic, game, and original IP teams plan and produce original stick-figure challenge content with model routing, sample generation, task tracking, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External content, animation, comic, game, and original IP teams use this skill to turn a stick-figure challenge brief into an original production plan, rights checklist, model and price lookup, sample generation flow, task record, and acceptance checklist. The workflow emphasizes original assets, readable action, scene continuity, and explicit approval before paid generation, batch operations, sending, or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External AI-HIVE MCP access is under-scoped, and the helper script can send API credentials to an endpoint selected by environment configuration.

Mitigation: Prefer the fixed AI-HIVE OAuth connector, keep API keys out of prompts and logs, and avoid AI_HIVE_MCP_URL unless the endpoint is fully trusted.

Risk: Paid generation, upload, batch, sending, or publication actions can create cost, expose user materials, or publish unintended outputs.

Mitigation: Require explicit confirmation before any paid generation, upload, batch action, sending, or public publication; use read-only model listing and existing task lookup before creating new jobs.

Risk: Reference works or user-supplied media may lack rights for public use or may lead to outputs that too closely copy protected material.

Mitigation: Maintain a material rights checklist, use references only for structure or functional goals, require original differences, and check character consistency, action readability, scene continuity, and IP originality before acceptance.

## Reference(s):

- [Original workflow card](artifact/references/original-workflow.md)
- [AI-HIVE MCP login and binding guide](artifact/references/mcp-binding.md)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-animation-109-572089f)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, optional shell commands, and local work-order JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use AI-HIVE MCP tools after user approval; paid generation, uploads, batch actions, sending, and public release require separate confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
