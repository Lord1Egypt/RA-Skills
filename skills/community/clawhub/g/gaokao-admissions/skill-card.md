## Description:

输入省份、分数、选科和家庭背景后，生成高考志愿位次换算、冲稳保院校清单、专业推荐和四年规划。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengjiangit](https://clawhub.ai/user/dengjiangit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and families in China can use this skill to prepare Gaokao admissions options by combining province, score, subject selection, rank, interests, and family context into a structured recommendation report. The skill is intended to support planning and comparison, not to replace official admissions data or human judgment.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Admissions recommendations, probability bands, school rankings, salary expectations, or score-to-rank conversions may be inaccurate or outdated.

Mitigation: Verify final decisions against official provincial exam authority data, university admissions pages, and current admissions plans.

Risk: Web search snippets or fallback reference data may be incomplete when live sources are unavailable.

Mitigation: Treat fallback outputs as planning estimates and label uncertain data before relying on it for application choices.

## Reference(s):

- [Province Gaokao Mode Reference](artifact/references/provinces.md)
- [University Classification and Subject Evaluation](artifact/references/universities.md)
- [Reach, Match, and Safety Scoring Model](artifact/references/scoring-model.md)
- [Major Outlook and Employment Analysis](artifact/references/career-outlook.md)
- [ClawHub Skill Page](https://clawhub.ai/dengjiangit/skills/gaokao-admissions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with ranked recommendations, probability bands, rationale, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are estimates based on public web data, local reference files, and fallback assumptions; final decisions should be verified against official admissions sources.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
