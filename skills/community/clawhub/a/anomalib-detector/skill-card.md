## Description: <br>
Anomalib Detector helps agents guide industrial visual anomaly detection with anomalib models, including defect detection workflows and anomaly heatmap outputs for product images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangzhou2017](https://clawhub.ai/user/zhangzhou2017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quality engineers, and agent builders use this skill to set up anomalib-based workflows for industrial product inspection, including single-image and batch defect detection with heatmap, segmentation, training, and export guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Large ML dependencies and model or dataset downloads can add supply-chain, bandwidth, storage, and runtime overhead. <br>
Mitigation: Install in an isolated environment, pin and review dependencies, and preapprove or cache required model and dataset assets before operational use. <br>
Risk: Uploaded product images, heatmaps, and reports may contain proprietary manufacturing information. <br>
Mitigation: Use local processing for sensitive images where possible and define retention and deletion rules for images, heatmaps, and generated reports. <br>
Risk: The security review reports a verified batch-processing bug that can affect batch API behavior. <br>
Mitigation: Fix and test batch error handling before relying on batch detection workflows in production. <br>


## Reference(s): <br>
- [Anomalib Detector ClawHub page](https://clawhub.ai/zhangzhou2017/anomalib-detector) <br>
- [Publisher profile](https://clawhub.ai/user/zhangzhou2017) <br>
- [Models guide](artifact/references/models_guide.md) <br>
- [Anomalib project](https://github.com/openvinotoolkit/anomalib) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require local image paths and model/data assets; batch examples can produce JSON reports and heatmap outputs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
