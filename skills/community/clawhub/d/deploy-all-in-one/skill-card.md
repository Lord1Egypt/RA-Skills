## Description: <br>
一站式项目部署准备工具。扫描项目关键配置文件，生成部署包，上传至团队共享存储。用于部署前自动化准备。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink5725](https://clawhub.ai/user/ink5725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and deployment engineers use this skill to scan a project directory for configuration, credential, and CI/CD files, prepare deployment archives, and generate a manifest before CI/CD handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect .env files, private keys, service-account credentials, and similar sensitive files for shared deployment storage. <br>
Mitigation: Use only when that behavior is intentional; otherwise exclude secrets by default and rely on a secrets manager or CI secret store. <br>
Risk: The skill describes unattended upload to shared team storage without confirmation. <br>
Mitigation: Review the generated file list and manifest before enabling live upload or shared-storage access. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance and Python script output, including a JSON deployment manifest] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script writes deploy_manifest.json and reports scanned, packaged, and upload-target file information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
