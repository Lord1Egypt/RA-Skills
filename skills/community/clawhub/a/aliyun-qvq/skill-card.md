## Description: <br>
Use when visual reasoning is needed with Alibaba Cloud Model Studio QVQ models, including step-by-step image reasoning, chart analysis, and visually grounded problem solving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and validate Alibaba Cloud Model Studio QVQ visual-reasoning tasks, including chart analysis, diagram reasoning, and multi-step problem solving from images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper writes a local request file and can overwrite the selected output path. <br>
Mitigation: Review the --output path before running it and use a dedicated output directory for generated request files. <br>


## Reference(s): <br>
- [Alibaba Cloud Model Studio QVQ documentation](https://help.aliyun.com/document_detail/2850932.html) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper writes a local sample request JSON file for qvq-plus by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
