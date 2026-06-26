## Description: <br>
Automates multi-coin spot grid trading on Bitget with dynamic adjustments, risk management, portfolio monitoring, and analysis tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hotflame-cloud](https://clawhub.ai/user/hotflame-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to configure and operate Bitget spot grid trading workflows, including starting and stopping grids, monitoring balances and orders, optimizing parameters, and generating reports. It should be used only by operators who can review exchange-account permissions and trading risk before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports plaintext Bitget credentials in the skill. <br>
Mitigation: Revoke any exposed credentials, remove them from local copies, and create new least-privilege keys with no withdrawal permission before use. <br>
Risk: The release evidence reports live order-changing scripts with weak safety boundaries. <br>
Mitigation: Review every script that can place, cancel, or modify orders, enable simulation or dry-run behavior where possible, and test with tightly limited balances before any live trading. <br>
Risk: Background or scheduled agents can continue trading after setup. <br>
Mitigation: Avoid enabling cron or background monitors until the operator has confirmed the exact account, symbols, permissions, and stop procedure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hotflame-cloud/bitget-data) <br>
- [Publisher Profile](https://clawhub.ai/user/hotflame-cloud) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript scripts, and JSON configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger Bitget API actions when generated commands or bundled scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
