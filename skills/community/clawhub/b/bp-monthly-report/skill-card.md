## Description: <br>
Draft monthly BP reports by normalizing templates, mapping BP anchors, collecting evidence, and writing sections in order with data-backed progress evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houtonghoutong](https://clawhub.ai/user/houtonghoutong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business planning and HR operations teams use this skill to draft monthly BP reports from a fixed template, BP period, node identifiers, and real BP or progress-report evidence. The workflow supports staged evidence collection, BP anchor mapping, traffic-light review, and review-ready monthly report artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access BP node data and month-specific business context that may be sensitive. <br>
Mitigation: Install and run it only when authorized to access the target BP node and reporting month. <br>
Risk: Generated manifests, review queues, and report files may contain internal report excerpts or personnel and business context. <br>
Mitigation: Write artifacts only to approved locations, protect access to generated files, and delete them when retention is not required. <br>
Risk: Helper scripts depend on trusted run inputs such as app keys, run directories, and output paths. <br>
Mitigation: Use only trusted app keys, trusted run directories, and approved output locations when executing helper scripts. <br>


## Reference(s): <br>
- [BP Monthly Report Skill](SKILL.md) <br>
- [Monthly Report Template v1](assets/P001-T001-MONTH-TPL-01_月报模板_v1.md) <br>
- [Monthly Report Fill Specification Example](assets/人力资源中心_月报填写规范_组织示例_v1.md) <br>
- [Workflow](references/workflow.md) <br>
- [BP System](references/bp-system.md) <br>
- [Source Schema](references/source-schema.md) <br>
- [Traffic Lights](references/traffic-lights.md) <br>
- [Artifact Layout](references/artifact-layout.md) <br>
- [BP System API Document](https://github.com/xgjk/dev-guide/blob/main/02.%E4%BA%A7%E5%93%81%E4%B8%9A%E5%8A%A1AI%E6%96%87%E6%A1%A3/BP/BP%E7%B3%BB%E7%BB%9FAPI%E8%AF%B4%E6%98%8E.md) <br>
- [BP System Business Document](https://github.com/xgjk/dev-guide/blob/main/02.%E4%BA%A7%E5%93%81%E4%B8%9A%E5%8A%A1AI%E6%96%87%E6%A1%A3/BP/BP%E7%B3%BB%E7%BB%9F%E4%B8%9A%E5%8A%A1%E8%AF%B4%E6%98%8E.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, structured intermediate artifacts, review queues, and helper script commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are grounded in BP anchors, progress evidence, fixed section ordering, and human-review traffic-light judgments.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
