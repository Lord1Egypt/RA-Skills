## Description: <br>
Analyzes user-provided cloud migration survey materials and generates a structured .docx survey report covering customer profile, current architecture, cloud product mapping, version compatibility risks, migration risks, and follow-up items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud architects, presales engineers, and migration delivery teams use this skill to turn supplied migration survey files into a structured Alibaba Cloud migration assessment report. It supports survey analysis from AWS, Azure, GCP, Huawei Cloud, Tencent Cloud, Baidu Cloud, or IDC environments to Alibaba Cloud, but does not perform migrations or create pricing proposals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically create reconstructed source files at user-provided paths when an input file is missing. <br>
Mitigation: Use it only in workspaces where automatic report generation is acceptable, and avoid paths where creating a new .xlsx, .docx, .csv, or .txt file would be surprising. <br>
Risk: Reports generated from reconstructed missing files may reflect incomplete prompt-provided details rather than authoritative source materials. <br>
Mitigation: Treat reconstructed-file reports as drafts and require review against authoritative survey evidence before relying on them. <br>
Risk: The generated migration report may include incorrect or outdated product mapping or compatibility guidance. <br>
Mitigation: Have a professional cloud architect review the report and confirm product mappings, version risks, and migration plans against current Alibaba Cloud documentation. <br>
Risk: Survey inputs may contain sensitive customer data. <br>
Mitigation: Review generated reports before sharing; the artifact includes red lines and quality checks intended to avoid secrets, real IPs, passwords, keys, and pricing content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-migration-mas-cloud-migration-survey) <br>
- [Cloud Product Mapping Reference](references/cloud-mapping.md) <br>
- [Version Compatibility Risk Reference](references/version-risks.md) <br>
- [Alibaba Cloud Cloud Migration Hub traffic replay documentation](https://help.aliyun.com/zh/cmh/cloud-migration-hub/traffic-replay) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with required shell commands and generated .docx report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Excel, Word, text, CSV, and JSON inputs through bundled Python scripts; generated reports are reference drafts requiring professional architect review.] <br>

## Skill Version(s): <br>
0.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
