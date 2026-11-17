## Description:

AI全维度营养顾问，基于用户画像和目标生成个性化饮食方案、慢病营养建议、中医体质食疗、运动营养策略、营养素解读、特殊人群指导、食物搭配建议和交互式 HTML 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to provide Chinese-focused nutrition education, meal planning, dietary guidance for common chronic conditions, sports nutrition advice, nutrient lookup, and optional local HTML reports. It is intended as educational support and not as a substitute for professional medical or registered dietitian advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store personal health profile details on disk.

Mitigation: Avoid entering unnecessary sensitive information and review or delete user_data/profile.json after use.

Risk: Generated HTML reports may include unescaped dynamic input.

Mitigation: Open generated reports only from trusted local inputs and avoid sharing or loading profile JSON from untrusted sources.

Risk: Nutrition guidance for chronic conditions and special populations can be misapplied as medical advice.

Mitigation: Treat outputs as educational guidance and consult a clinician or registered dietitian for diagnosis, treatment, pregnancy, pediatric, elder-care, or chronic-condition decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/ai-nutritionist)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown guidance with optional shell commands and local HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local profile JSON and HTML report files when the user asks for stored profile data or a report.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
