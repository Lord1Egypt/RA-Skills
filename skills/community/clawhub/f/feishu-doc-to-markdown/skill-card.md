## Description:

智能转换飞书文档为高可用Markdown格式，自动处理私有资源、无效占位符、冗余引用，生成多版本满足不同场景需求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[whisperbot](https://clawhub.ai/user/whisperbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-management users use this skill to convert Feishu documents into Markdown for archiving, knowledge-base import, core-point extraction, and document cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted Feishu document contents and metadata can persist as local raw backups, summaries, and archived Markdown files.

Mitigation: Before installing or running the skill, confirm that local output paths, auto_archive settings, and retention expectations are acceptable for the documents being converted.

Risk: Knowledge-base sync can copy sensitive document summaries or core points into another persistent destination.

Mitigation: Enable knowledge-base sync only when the destination permissions and retention policy are appropriate for the source documents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/whisperbot/skills/feishu-doc-to-markdown)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration]

**Output Format:** [Markdown documents with optional local archive files and knowledge-base entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports raw, enhanced, and optimized output versions; converted content may be archived locally or synced to LEARNINGS.md when configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
