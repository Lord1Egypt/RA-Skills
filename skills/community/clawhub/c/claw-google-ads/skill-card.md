## Description: <br>
Manages Google Ads campaigns through the Google Ads API, including viewing campaign metrics, adjusting daily budgets, changing campaign status, and generating basic reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[3824108-cell](https://clawhub.ai/user/3824108-cell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect Google Ads campaign performance and run campaign-management commands through a local Python script. It is intended for accounts where the user can provide Google Ads API credentials and confirm sensitive campaign changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Google Ads API credentials and may access ad-account data. <br>
Mitigation: Use dedicated least-privilege credentials where possible and protect the ~/.google-ads.yaml configuration file. <br>
Risk: The tool may select the first accessible Google Ads customer account by default. <br>
Mitigation: Verify the selected customer account before listing data or making campaign changes. <br>
Risk: Budget and campaign-status commands can materially affect advertising spend or campaign availability. <br>
Mitigation: Require explicit confirmation before any budget update or campaign enable/disable action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/3824108-cell/claw-google-ads) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Google Ads API credentials; budget and campaign-status changes should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
