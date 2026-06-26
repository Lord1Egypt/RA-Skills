## Description: <br>
文章风格深度分析与模仿指南生成。当用户提供一篇或多篇文章样本，要求分析写作风格、提取风格特征、生成模仿指南、或按某种风格创作新内容时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengxiaotian](https://clawhub.ai/user/pengxiaotian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and writing assistants use this skill to analyze one or more article samples, extract stable style traits, and create a structured imitation guide for style-inspired writing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided samples may contain text the user does not have rights to provide. <br>
Mitigation: Use only article samples the user has the right to provide. <br>
Risk: Style-inspired output can be mistaken for text written or endorsed by the original author. <br>
Mitigation: Clearly label generated content as style-inspired and do not present it as written or endorsed by the original author. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengxiaotian/article-style-analyzer) <br>
- [分析维度详解](artifact/references/analysis-dimensions.md) <br>
- [输出 Schema](artifact/references/output-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON analysis with text guidance for style imitation tasks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-article outputs omit cross-text constant features and style-change analysis; multi-article outputs include the full schema.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
