## Description:

使用 ArkCLI 创建、校验、查询、更新、删除、版本化和下载 Dataset。用户提到 Dataset、数据集、ds-*、dsv-*、训练集/验证集复用、数据格式校验或把 Dataset 接入精调任务时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

开发者使用此技能通过 ArkCLI 管理可复用的精调数据集，包括创建和校验数据、维护版本、下载数据，以及将 Dataset 版本引用接入精调任务。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced shared ArkCLI guidance file is missing from the supplied release evidence, so its authentication, output, and confirmation rules are not available here.

Mitigation: Review the applicable shared ArkCLI guidance and linked materials before installation, as recommended by the security guidance.

Risk: Dataset creation, updates, downloads, and deletion can affect remote data or local files.

Mitigation: Use the supported --dry-run preview where available; before deletion, review the displayed impact and confirm separately.

## Reference(s):

- [Dataset command workflows](artifact/references/commands.md)
- [Dataset skill evaluation cases](artifact/references/evals.md)
- [ArkCLI Datasets on ClawHub](https://clawhub.ai/jasonstarlight/skills/arkcli-datasets)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use workflow-specific inputs such as JSONL files, TOS URIs, model identifiers, and Dataset or version IDs.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
