## Description:

Use when drafting a monthly BP report from a fixed template, BP period and node identifiers, and real BP or progress-report evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houtonghoutong](https://clawhub.ai/user/houtonghoutong)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to draft BP monthly reports that follow a fixed template, align to BP goals and key results, and cite real progress evidence. Developers or reporting operators can also use its helper workflow to collect evidence, build section cards, and produce reviewable report artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts handle internal BP report data and credentials.

Mitigation: Install only in a trusted BP reporting environment and use a dedicated least-privilege API key.

Risk: Credentials could be exposed through shell history or shared scripts.

Mitigation: Avoid placing API keys directly in command history or shared script files.

Risk: Generated outputs may write or overwrite files with weak path controls.

Mitigation: Write outputs only to a private dedicated directory and avoid running artifact builders on untrusted run directories until path containment and safe YAML parsing are fixed.

## Reference(s):

- [BP Monthly Report Skill](artifact/SKILL.md)
- [Workflow](artifact/references/workflow.md)
- [BP System](artifact/references/bp-system.md)
- [Source Schema](artifact/references/source-schema.md)
- [Artifact Layout](artifact/references/artifact-layout.md)
- [Section Order](artifact/references/section-order.md)
- [Traffic Lights](artifact/references/traffic-lights.md)
- [Fill Patterns](artifact/references/fill-patterns.md)
- [Rolling Baseline](artifact/references/rolling-baseline.md)
- [BP Monthly Report Template v1](artifact/assets/P001-T001-MONTH-TPL-01_月报模板_v1.md)
- [Monthly Report Fill Specification Example v1](artifact/assets/人力资源中心_月报填写规范_组织示例_v1.md)
- [BP System API Documentation](https://github.com/xgjk/dev-guide/blob/main/02.%E4%BA%A7%E5%93%81%E4%B8%9A%E5%8A%A1AI%E6%96%87%E6%A1%A3/BP/BP%E7%B3%BB%E7%BB%9FAPI%E8%AF%B4%E6%98%8E.md)
- [BP System Business Documentation](https://github.com/xgjk/dev-guide/blob/main/02.%E4%BA%A7%E5%93%81%E4%B8%9A%E5%8A%A1AI%E6%96%87%E6%A1%A3/BP/BP%E7%B3%BB%E7%BB%9F%E4%B8%9A%E5%8A%A1%E8%AF%B4%E6%98%8E.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown reports with YAML, JSON, and Markdown intermediate artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged evidence ledgers, BP anchor maps, fine-grained cards, AI baseline reports, review queues, and user review reports.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
