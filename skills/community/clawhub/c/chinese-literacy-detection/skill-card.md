## Description:

Chinese Literacy Detection guides an agent through a conversational Chinese-character literacy assessment for children aged 3-12 using stratified sampling, adaptive stopping, and score reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwang4git](https://clawhub.ai/user/wangwang4git)

### License/Terms of Use:

MIT-0

## Use Case:

Parents, guardians, educators, and agent users use this skill to estimate a child's Chinese-character recognition level, produce a positive assessment report, and optionally review unfamiliar characters. Developers can also use the included references and helper scripts to validate data, sampling, and scoring behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for child literacy assessment and may handle age and performance details.

Mitigation: Review privacy, consent, and guardian-notice requirements before using the skill with children or retaining assessment results.

Risk: The skill automatically promotes an opaque WeChat mini-program QR code according to the security summary.

Mitigation: Verify the QR code destination and provide clear privacy and consent information before showing it to users.

## Reference(s):

- [Algorithm Specification](artifact/references/algorithm-spec.md)
- [Data Schema](artifact/references/data-schema.md)
- [Chatbot Workflow](artifact/references/chatbot-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/wangwang4git/skills/chinese-literacy-detection)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown conversation prompts, assessment tables, score reports, review guidance, and optional helper-script command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a bundled JSON data asset of 2500 Chinese characters and local Python helper scripts for validation, sequence generation, and score calculation.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
