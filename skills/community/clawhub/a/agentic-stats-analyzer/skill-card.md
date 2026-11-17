## Description:

对候选队列执行描述性统计与组间比较，生成感染率对比、描述统计表、结果摘要与论文框架草案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergenceronearth](https://clawhub.ai/user/emergenceronearth)

### License/Terms of Use:

MIT-0

## Use Case:

科研或医疗数据分析用户可用此技能读取预期的 analysis.json 数据，生成候选队列的描述性统计、组间感染率比较、关键发现摘要和论文框架草案。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a fixed local analysis.json path and may fail or expose unintended local data if that path is not the expected demo dataset.

Mitigation: Install only in environments where /home/ubuntu/workspace/demo/mock_data/analysis.json is expected and contains approved data for analysis.

Risk: The skill sends start and completion status messages to a localhost reporting endpoint.

Mitigation: Use it only when the local reporting service on localhost:5001 is expected, or review the reporting behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emergenceronearth/skills/agentic-stats-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tables, bullet summaries, paper-outline sections, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads the expected analysis.json data file and reports start/completion status to localhost when that local reporting service is present.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
