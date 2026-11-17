## Description:

书匠编排 5 个小说创作智能体，生成带热点洞察、人物设计、剧情设计、正文写作、质量闸门和可追溯工件的端到端中文言情创作流水线。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dai-chaoyu](https://clawhub.ai/user/dai-chaoyu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent operators use this skill to coordinate Chinese romance-novel ideation, drafting, QA, revision loops, and artifact tracking across a multi-agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad command, browsing, editing, and agent-delegation capabilities.

Mitigation: Run it in a sandboxed workspace with only the needed tool permissions enabled, and review generated actions before execution.

Risk: The workflow can create and overwrite project files.

Mitigation: Use a fresh project directory, keep backups for important work, and review filenames before allowing file writes.

Risk: The hotspot crawler browses listed novel-ranking sites and may depend on changing external pages.

Mitigation: Treat retrieved trend data as time-sensitive, record unavailable sources, and review citations or URLs before using the output.

Risk: The security verdict is suspicious because requested powers are not tightly controlled.

Mitigation: Avoid giving the skill sensitive directories, secrets, or credentials, and inspect generated artifacts before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dai-chaoyu/skills/booksmith-orchestrator)
- [Publisher profile](https://clawhub.ai/user/dai-chaoyu)
- [Zongheng ranking](https://www.zongheng.com/rank)
- [JJWXC top ten](https://www.jjwxc.net/topten.php)
- [Fanqie Novel ranking](https://fanqienovel.com/rank)
- [Qidian ranking](https://www.qidian.com/rank)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown and JSON project files with a concise final text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-scoped hotspot JSON, character sheets, plot blueprints, manuscript files, quality reports, iteration logs, and execution context snapshots.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
