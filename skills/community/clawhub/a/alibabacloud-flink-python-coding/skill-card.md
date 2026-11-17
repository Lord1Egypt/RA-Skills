## Description:

Helps developers write, modify, review, and debug PyFlink jobs on Alibaba Cloud VVR, answer API questions, resolve dependencies, and prepare deployment artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to develop, troubleshoot, and prepare PyFlink jobs for Alibaba Cloud Realtime Compute for Apache Flink (VVR 11.8 or newer), including API selection and dependency planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated sink or deployment example may overwrite data when run on VVR.

Mitigation: Review generated jobs and sink settings, especially overwrite behavior, before deployment.

Risk: Secrets placed in source files or handoff documentation may be exposed.

Mitigation: Keep real credentials in Alibaba Cloud secret variables rather than source files or README text.

Risk: Dependency inspection may download versioned PyFlink wheels.

Mitigation: Review requested downloads and confirm the target version before inspecting packages.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-flink-python-coding)
- [Official documentation guide](references/official-docs.md)
- [VVR release notes](https://help.aliyun.com/zh/flink/realtime-flink/product-overview/release-notes)
- [Python job development](https://help.aliyun.com/zh/flink/realtime-flink/user-guide/develop-a-pyflink-job)
- [PyFlink DataFrame API reference](https://ververica-flink-docs.readthedocs.io/en/latest/reference/pyflink.dataframe/index.html)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, Files]

**Output Format:** [Text and Markdown with PyFlink code, commands, and local deployment files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local job and handoff artifacts; cloud submission is separate.]

## Skill Version(s):

0.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
