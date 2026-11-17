## Description:

A Chinese-language entertainment fortune-telling assistant that generates BaZi charts, astrology readings, face-reading and palm-reading interpretations, with cross-validation against classical reference material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2584894611-debug](https://clawhub.ai/user/2584894611-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for entertainment-oriented Chinese metaphysics readings based on birth details and optional face or palm photos. The skill is not appropriate for medical, hiring, relationship, financial, legal, or other important decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may request sensitive birth information, gender, and face or palm photos.

Mitigation: Collect only information the user chooses to provide, avoid uploading photos of other people without consent, and do not retain or reuse images beyond the session need.

Risk: The skill can produce unsupported health, lifespan, character, relationship, financial, or legal-adjacent judgments from fortune-telling or photos.

Mitigation: Keep outputs framed as entertainment and cultural reference, avoid deterministic claims, and direct users not to rely on readings for important decisions.

Risk: The server security verdict is suspicious despite no executable install behavior.

Mitigation: Review the skill before deployment and ensure its safeguards align with privacy and high-stakes decision policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2584894611-debug/skills/cyber-fortune-teller)
- [Skill homepage](https://xiaping.coze.site/skill/dc152af5-1641-4b74-9a5f-ad34bf71ed67)
- [BaZi analysis flow](references/bazi-flow.md)
- [Face-reading analysis flow](references/face-flow.md)
- [Palm-reading analysis flow](references/palm-flow.md)
- [Three-system cross-validation rules](references/cross-validation.md)
- [三命通会](references/三命通会.md)
- [子平真诠](references/子平真诠.md)
- [易经杂说](references/易经杂说.md)
- [柳庄神相](references/柳庄神相.md)
- [渊海子平](references/渊海子平.md)
- [滴天髓](references/滴天髓.md)
- [神相全编](references/神相全编.md)
- [穷通宝鉴](references/穷通宝鉴.md)
- [风水学](references/风水学.md)
- [麻衣神相](references/麻衣神相.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown-style readings and advice.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request birth date, birth time, birthplace, gender, and optional face or palm photos; outputs should remain entertainment guidance.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact frontmatter is 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
