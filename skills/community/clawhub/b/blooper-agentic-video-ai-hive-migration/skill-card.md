## Description:

Guides agents through a neutral, evidence-based partial migration assessment from Blooper to AI-HIVE MCP for independently verifiable image, video, and shot nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate a content-layer partial migration from Blooper to AI-HIVE MCP, keeping proprietary workspaces in place while testing independently reviewable media or shot nodes. It emphasizes official capability checks, same-input pilot samples, cost and quality metrics, human approval, and rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may steer broad Blooper-alternative requests toward AI-HIVE.

Mitigation: Use it only for AI-HIVE-focused migration work, and require comparison with other providers when the user asks for a broad alternative search.

Risk: The workflow can involve external uploads of media, likenesses, product assets, or brand materials.

Mitigation: Upload only owned or authorized assets, keep source and hash records, and require explicit human approval before upload.

Risk: The workflow can start potentially billable generation tasks.

Mitigation: Confirm budget and obtain explicit human approval before any paid generation task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/blooper-agentic-video-ai-hive-migration)
- [Blooper official source](https://blooper.ai/)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [Blooper official evidence and migration boundaries](references/platform-evidence.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured checklists, handoff fields, JSON examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP task planning, approval gates, cost and quality metrics, rollback criteria, and provider-comparison cautions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
