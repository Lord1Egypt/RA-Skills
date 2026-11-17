## Description:

Industrial vision anomaly detection for product images using anomalib models, returning defect classifications, anomaly scores, and heatmap-style visual outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangzhou2017](https://clawhub.ai/user/zhangzhou2017)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and industrial quality engineers use this skill to inspect product images for visual defects, tune anomalib model choices, run single-image or batch anomaly detection, and prepare model training or export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A single-image request may process other images in the same directory.

Mitigation: Use isolated per-request input directories and avoid folders containing unrelated or sensitive images.

Risk: Uploaded image storage, result URLs, access control, retention, and deletion behavior are under-specified.

Mitigation: Define and enforce storage location, result access, retention, and deletion controls before production use.

Risk: Unpinned dependencies may change model behavior or introduce supply-chain exposure.

Mitigation: Pin and lock dependencies, then scan the resolved environment before production deployment.

## Reference(s):

- [Anomalib Detector on ClawHub](https://clawhub.ai/zhangzhou2017/skills/anomalib-detector)
- [Publisher profile](https://clawhub.ai/user/zhangzhou2017)
- [Model selection guide](references/models_guide.md)
- [Anomalib project](https://github.com/openvinotoolkit/anomalib)
- [MVTec AD dataset](https://www.mvtec.com/company/research/datasets/mvtec-ad/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and Python-oriented guidance with shell commands, configuration snippets, JSON-like result examples, and anomaly detection report structures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe image anomaly scores, boolean defect labels, heatmaps, segmentation masks, batch summaries, and model export options.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
