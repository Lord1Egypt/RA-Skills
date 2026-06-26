## Description: <br>
Automates Let's Encrypt SSL certificate issuance, renewal, status checks, and Windows scheduled renewal using Baidu Cloud DNS validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xzhower](https://clawhub.ai/user/xzhower) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to obtain and renew Let's Encrypt certificates for domains hosted on Baidu Cloud DNS, including wildcard certificates and scheduled renewal workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes an unrelated Gitee publishing script with a hardcoded token. <br>
Mitigation: Remove upload_skill.py before installation and rotate or revoke the exposed token if it is real. <br>
Risk: The skill requires Baidu DNS credentials and stores configuration in config.conf. <br>
Mitigation: Use a least-privilege DNS key limited to the target zone and restrict write access to config.conf and the skill directory. <br>
Risk: The renewal hook can execute a configured shell command after certificate renewal. <br>
Mitigation: Leave RENEW_HOOK unset unless the command is fully trusted and reviewed. <br>
Risk: The Windows scheduled-task helper registers renewal with elevated SYSTEM privileges. <br>
Mitigation: Run scheduled renewal under the least-privileged account that can perform the task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xzhower/bce-cert-skill-pkg) <br>
- [Project source link](https://gitee.com/x-hower/bce-cert) <br>
- [Let's Encrypt](https://letsencrypt.org/) <br>
- [Baidu Cloud](https://cloud.baidu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local certificate files, account keys, DNS TXT records, renewal logs, and Windows scheduled-task commands when the packaged scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
