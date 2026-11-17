## Description:

帮助开发者比对数据契约与采集、落盘和读取环节的字段名，定位静默丢数并通过回归测试防止再次漂移。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

开发者和数据工程师可用它排查字段为空、回填无效或记录静默消失的问题，并设计契约名回归测试与回填对账。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying the checklist to an unrelated issue may lead to unnecessary data changes.

Mitigation: Confirm a field-name mismatch across the data contract, writer, stored records, and reader before changing data.

Risk: Backfills can overwrite records or leave derived outputs inconsistent.

Mitigation: Review commands, dry-run and back up data, fill only missing values, then reconcile counts and downstream results.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/oracis/skills/data-pipeline-field-drift)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with inline shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Debugging checklist, contract-key regression tests, and backfill verification steps]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
