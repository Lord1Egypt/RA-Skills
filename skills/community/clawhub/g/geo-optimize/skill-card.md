## Description: <br>
GEO优化工具——语义训练+内容创作。适用于执行GEO概念相关工作，以及创建高质量文章的场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Maschera96](https://clawhub.ai/user/Maschera96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and marketers use this skill to plan and draft Chinese GEO-optimized articles after providing one to three keywords, with platform-specific guidance for Xiaohongshu, WeChat, Zhihu, and Toutiao. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for broad writing prompts and draft content before the user has fully specified intent. <br>
Mitigation: Confirm the requested keywords, platform, and output location before drafting, especially when the user asks for general article writing. <br>
Risk: Generated GEO or marketing content may include inaccurate claims or unsuitable publication guidance. <br>
Mitigation: Review facts, sources, brand claims, and platform requirements before publishing or relying on the draft. <br>
Risk: The skill may create draft files under geo-output/articles/ by default. <br>
Mitigation: Specify inline-only output or a different path when file creation is not desired. <br>


## Reference(s): <br>
- [GEO Optimization Guide](geo-optimization.md) <br>
- [ClawHub release page](https://clawhub.ai/Maschera96/geo-optimize) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown article drafts and content guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write article drafts under geo-output/articles/ unless the user requests inline output or another path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
