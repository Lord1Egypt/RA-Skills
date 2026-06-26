## Description: <br>
Helps agents configure package-manager mirrors for pip, npm, yarn, pnpm, cargo, Go modules, NuGet, RubyGems, Conda, Homebrew, Gradle, Maven, and Composer when users need faster dependency downloads in mainland China. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[normdist-ai](https://clawhub.ai/user/normdist-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to identify relevant package managers, choose suitable mainland China mirror services, apply global or project-level mirror configuration, and verify the resulting package-manager settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permanently redirect future package downloads through third-party mirrors and overwrite existing package-manager settings. <br>
Mitigation: Confirm the selected package managers, mirror providers, and configuration scope before execution; prefer project-level configuration where practical. <br>
Risk: Mirror choices may conflict with workplace security policy or software supply-chain requirements. <br>
Mitigation: Verify that Aliyun, Huawei Cloud, Tsinghua, USTC, Tencent Cloud, or other selected mirrors are approved for the user's environment. <br>
Risk: Existing package-manager and shell configuration files may be changed. <br>
Mitigation: Back up existing package-manager and shell configuration files before applying global settings, then run the documented verification commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/normdist-ai/china-mirrors) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/normdist-ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, PowerShell, XML, and Groovy code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include environment checks, package-manager mirror settings, verification commands, and restore-default commands.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
