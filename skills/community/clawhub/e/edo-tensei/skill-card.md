## Description:

edo-tensei is a Chinese-language WorkBuddy skill for splitting large agent sessions into focused handoff sessions, onboarding scattered sessions into a traceable control tower, and exporting or importing workspace subtrees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bug-belief](https://clawhub.ai/user/bug-belief)

### License/Terms of Use:

MIT License（含署名保留条款）

## Use Case:

Developers and agent users use this skill to manage long-running or multi-session work by creating control-tower indexes, handoff documents, dependency maps, export packages, and import workflows for WorkBuddy projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports that the ZIP import script can write outside the chosen workspace if a crafted migration package is imported.

Mitigation: Do not import ZIP packages from other people or untrusted workspaces until path traversal and pre-write verification are fixed; review package contents before import.

Risk: Exported handoff packages may contain sensitive project files or private links.

Mitigation: Inspect exported packages and handoff documents before sharing them outside the intended workspace or team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bug-belief/skills/edo-tensei)
- [Publisher profile](https://clawhub.ai/user/bug-belief)
- [Control Tower Mechanism](references/控制塔机制.md)
- [Project Index Template](references/INDEX模板.md)
- [Session Handoff Template](references/会话上下文交接模板.md)
- [Dependency DAG and Action Board](references/依赖图谱与行动看板.md)
- [Cross-Platform Migration Toolkit](references/跨平台移植工具包.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with file templates, inline shell commands, and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are primarily Chinese-language handoff, index, dependency, export, import, and configuration artifacts for WorkBuddy workspaces.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, manifest.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
