## Description:

AI急救指南 helps agents provide Chinese-language, structured first-aid reference guidance across CPR/AED, choking, bleeding, burns, poisoning, environmental emergencies, medical emergencies, bites, outdoor incidents, first-aid kits, and certification topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese-language first-aid questions, select relevant first-aid reference material, and optionally generate a standalone HTML first-aid report for complex requests.

### Deployment Geography for Use:

China / Chinese-language contexts

## Known Risks and Mitigations:

Risk: Emergency medical guidance may be unsafe, outdated, or under-scoped for a user's specific condition.

Mitigation: Review and correct medical content against current certified first-aid sources before deployment, and preserve clear escalation to professional emergency services.

Risk: The skill is oriented around Chinese-language emergency guidance and the 120 emergency number, which may be inappropriate in other locales.

Mitigation: Use it for China or Chinese-language contexts unless locale selection and local emergency-number handling are added and reviewed.

Risk: Generated HTML reports could make first-aid guidance appear more authoritative than the reviewed source material supports.

Mitigation: Keep disclaimers, medical-review status, emergency escalation, and limits of first-aid advice visible in generated reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/first-aid-guide)
- [心肺复苏 (CPR) 与 AED 使用指南](references/cpr-aed.md)
- [海姆立克急救法 (Heimlich Maneuver)](references/heimlich.md)
- [止血、包扎与骨折固定指南](references/trauma.md)
- [烧伤急救指南](references/burns.md)
- [中毒急救指南](references/poisoning.md)
- [环境急症急救：中暑、失温与溺水](references/environmental.md)
- [内科急症识别与急救：癫痫、心梗、卒中](references/medical-emergency.md)
- [动物咬伤与户外急救指南](references/bites-outdoor.md)
- [家庭急救包与急救证指南](references/kit-certification.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with optional standalone HTML report code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language, emergency-oriented responses that should include medical disclaimers and escalation to professional emergency services.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
