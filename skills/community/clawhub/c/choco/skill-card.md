## Description: <br>
Chocolatey operations integration for post-upgrade checks, NSSM service path refreshes, NSSM-to-shawl migration guidance, and recovery from stale Chocolatey or UniGetUI metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Windows administrators use this skill to diagnose Chocolatey-managed Windows service issues, generate commands for NSSM path repair, plan NSSM-to-shawl migrations, and resynchronize stale Chocolatey package metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Elevated Chocolatey, NSSM, shawl, and Windows service commands can change or remove services. <br>
Mitigation: Review each proposed command, confirm the target service and executable path, and use a maintenance window with a rollback plan for production services. <br>
Risk: Service re-registration can expose or mishandle service-account credentials. <br>
Mitigation: Do not paste passwords into chat or hardcode them in scripts; use secure prompts or managed service accounts where possible. <br>
Risk: Downloading shawl from a release URL introduces binary supply-chain risk. <br>
Mitigation: Verify the downloaded shawl binary independently before installing or using it. <br>
Risk: Incorrect service account or path choices can break sync services or change file ownership behavior. <br>
Mitigation: Preserve existing service settings during migration and verify service status, account, path, and application behavior after changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/skills/choco) <br>
- [Chocolatey documentation](https://docs.chocolatey.org/) <br>
- [UniGetUI repository](https://github.com/Devolutions/UniGetUI) <br>
- [shawl repository](https://github.com/mtkennerly/shawl) <br>
- [chocolatey/choco repository](https://github.com/chocolatey/choco) <br>
- [Syncthing v2.0 release notes](https://github.com/syncthing/syncthing/releases/tag/v2.0.0) <br>
- [Syncthing issue 10340](https://github.com/syncthing/syncthing/issues/10340) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell, PowerShell, and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose elevated Windows service and Chocolatey commands for human review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and CHANGELOG, released 2026-06-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
