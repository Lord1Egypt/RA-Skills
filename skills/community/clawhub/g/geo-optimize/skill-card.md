## Description:

geo-optimize helps agents create GEO-oriented content and article drafts using keyword-driven structure, semantic optimization, and platform-specific writing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maschera96](https://clawhub.ai/user/maschera96)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to draft GEO-optimized articles and social content after providing one to three target keywords. It supports Chinese content workflows and adapts draft structure for platforms such as Xiaohongshu, WeChat, Zhihu, and Toutiao when a platform is specified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad writing or GEO-related phrases when a user did not intend to use this workflow.

Mitigation: Review or adjust activation phrases so the skill runs only for explicit GEO or content-creation requests.

Risk: Generated content can contain unsupported claims or weak source attribution if the user provides sparse inputs.

Mitigation: Require target keywords before drafting and review factual claims, examples, and citations before publication.

## Reference(s):

- [GEO Optimization Guide](artifact/geo-optimization.md)
- [ClawHub Skill Page](https://clawhub.ai/maschera96/skills/geo-optimize)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown article content and concise writing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated markdown articles under geo-output/articles/ unless the user requests a different output style.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
