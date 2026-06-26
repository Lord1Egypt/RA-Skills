## Description: <br>
Automates viral short-video replication workflows for Douyin and other short-video platforms by analyzing product or media inputs, uploading reference assets, and generating similarly styled video outputs through VolcEngine Kickart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketing or content teams use this skill to create short-form promotional videos that follow a provided popular video's structure and style. The workflow covers VolcEngine/Kickart authentication, plan checks, material upload, product and creative analysis, reference video handling, optional digital avatar assets, task polling, and generated video result delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires VolcEngine/Kickart credentials and can access external account capabilities. <br>
Mitigation: Use scoped, temporary credentials or a platform secret store, and do not paste long-lived cloud secrets into chat. <br>
Risk: The workflow uploads and processes media assets that may be private, copyrighted, or business-sensitive. <br>
Mitigation: Review the publisher, media-retention behavior, local logs, and rights to the source material before using sensitive assets. <br>
Risk: The skill performs external plan, package, task submission, update, and polling actions. <br>
Mitigation: Confirm the account plan, package-registration or update steps, and background polling behavior before installation or production use. <br>
Risk: Generated video outputs may need compliance, rights, and sensitivity review before publication. <br>
Mitigation: Review generated outputs and follow the referenced Kickart compliance prompts before distributing the resulting content. <br>


## Reference(s): <br>
- [Authentication guide](references/火山鉴权指南.md) <br>
- [Plan activation guide](references/套餐开通指南.md) <br>
- [Material upload guide](references/素材上传指南.md) <br>
- [Material analysis guide](references/素材分析指南.md) <br>
- [Creative analysis guide](references/创意分析指南.md) <br>
- [Viral replication guide](references/爆款裂变指南.md) <br>
- [Reference video guide](references/视频参考指南.md) <br>
- [Digital avatar guide](references/数字形象指南.md) <br>
- [Task query guide](references/任务查询指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown guidance with shell commands, JSON result files, media asset identifiers, task identifiers, and generated video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VolcEngine/Kickart credentials and a valid plan; outputs may include local JSON paths, remote media IDs, task status messages, and generated video download URLs.] <br>

## Skill Version(s): <br>
1.0.5 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
