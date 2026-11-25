## Description:

当数据流水线里某个字段「一直读不到」、某类条目静默消失、或下游把「有数据」当成「没数据」时，用契约名比对法定位字段名漂移（同一逻辑字段在采集/暂存/落盘/读取四处各有一个名字），并写「契约名回归测试」钉死。含 grep 排查模板、死变量识别、回填对账顺序。当用户说「这个字段怎么一直是空的」「数据明明有却读不到」「回填没效果」「某类记录莫名不见了」时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

供开发者和数据工程师在数据源已有数据、但字段仍为空、记录静默消失或回填无效时使用。通过比对字段契约在采集、暂存、落盘和读取环节的名称，定位漂移并补充回归测试与安全回填核对步骤。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports no findings and a benign verdict with medium confidence, but some referenced paths were unavailable and the bundled image was outside scan coverage.

Mitigation: Review the referenced materials and image before installing, as advised by the security evidence.

Risk: Following backfill guidance can modify stored data.

Mitigation: Use the documented dry-run first, back up the data before a live run, and reconcile the updated counts and field coverage afterward.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oracis/skills/data-pipeline-field-drift)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline grep, shell, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes field-comparison checklists, regression-test examples, and a backfill verification sequence.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
