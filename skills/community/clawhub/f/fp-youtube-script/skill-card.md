## Description:

输入视频主题、关键词和产品信息，生成 5 分钟 YouTube 维修科普视频的 10 列中英分镜脚本，并内置技术准确性和安全提示规范。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuxirui677](https://clawhub.ai/user/zhuxirui677)

### License/Terms of Use:

MIT-0

## Use Case:

Content and operations teams creating FridayParts-style heavy-equipment repair videos use this skill to turn a topic, keywords, and product information into a structured bilingual shot-by-shot script. The output is intended as a draft for technical review before filming or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated repair explanations or product-fit details may be inaccurate or incomplete.

Mitigation: Have technical staff verify working principles, inspection steps, safety warnings, and product model fit before publication.

Risk: The skill uses broad video-script triggers and a model setting selected for branded repair-script generation.

Mitigation: Review the triggers and model configuration before import, and install only when a FridayParts-branded repair-video script generator is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhuxirui677/skills/fp-youtube-script)
- [Publisher Profile](https://clawhub.ai/user/zhuxirui677)
- [README](artifact/README.md)
- [Skill Definition](artifact/skill/SKILL.md)
- [Human Verification Checklist](artifact/reference/人工验证checklist.md)
- [Example Output: Water Pump vs Thermostat](artifact/examples/example_water_pump_thermostat.md)
- [Validation Comparison](artifact/examples/对比说明_规范生效验证.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown table with bilingual script text, image-generation prompts, and shot guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets 5-minute repair explainer scripts, approximately 750-850 English voiceover words, using fixed HOOK, BODY, SUMMARY, and ENDING sections.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter says 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
