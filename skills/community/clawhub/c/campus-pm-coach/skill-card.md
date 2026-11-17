## Description:

校招/实习互联网产品经理简历评分与面试模拟技能，可按 5 维度能力体系评估简历、生成防幻觉优化稿，并基于 JD 输出模拟面试题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[winkychannn](https://clawhub.ai/user/winkychannn)

### License/Terms of Use:

MIT-0

## Use Case:

External candidates and career-support agents use this skill to review campus or internship product-manager resumes against a target JD, improve the resume without inventing experience, and prepare likely interview questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume PDFs or images may send sensitive resume content to Tencent Cloud OCR.

Mitigation: Use text input when possible, install only in a controlled environment, and verify TENCENTCLOUD_ENDPOINT is not overridden before OCR use.

Risk: Shipped legacy helpers can fetch URLs or install packages at runtime.

Mitigation: Avoid invoking legacy ocr_utils.py or llm_client.py unless they are reviewed or removed, and preinstall pinned dependencies instead of allowing runtime installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/winkychannn/skills/campus-pm-coach)
- [Skill documentation](SKILL.md)
- [Scoring dimensions](config/default_dimensions.json)
- [Interview question templates](config/interview_templates.json)
- [Runtime requirements](scripts/requirements.txt)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown reports and JSON scoring results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include a quick diagnosis, detailed scoring report, optimized resume draft, scoring JSON, and mock interview question set.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
