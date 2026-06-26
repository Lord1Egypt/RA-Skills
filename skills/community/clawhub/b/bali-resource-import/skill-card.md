## Description: <br>
Guides agents through parsing Bali supplier documents and appending standardized tourism resource records to existing CSV libraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[errsr](https://clawhub.ai/user/errsr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel operations teams and their agents use this skill to parse Bali supplier contracts or resource files, standardize hotel, vehicle, attraction, activity, spa, club, restaurant, and afternoon-tea records, and append them to existing CSV resource libraries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify production CSV files. <br>
Mitigation: Use a dedicated temporary target folder, back up CSVs first, and require a dry run or preview before appending records. <br>
Risk: Cleanup behavior can delete files in a chosen folder. <br>
Mitigation: Restrict cleanup to files created during the current run and verify the target directory before execution. <br>
Risk: Redis broadcasting is included but may be unnecessary for many imports. <br>
Mitigation: Disable or remove Redis broadcasting unless the deployment explicitly requires resource update notifications. <br>


## Reference(s): <br>
- [巴厘岛旅游资源标准化文档体系](artifact/references/旅游资源标准化文档体系.md) <br>
- [ClawHub skill release](https://clawhub.ai/errsr/bali-resource-import) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated CSV-oriented code or data instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can append rows to existing CSV files when executed with user-provided source and target paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
