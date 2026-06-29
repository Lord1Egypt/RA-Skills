## Description: <br>
Price Monitor Skill is a Lite ecommerce price search skill for manual Taobao and Pinduoduo comparisons and basic price reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[since198905](https://clawhub.ai/user/since198905) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run manual ecommerce price searches for configured or prompted keywords across Taobao and Pinduoduo and review basic comparison results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes broader monitoring and notification behavior beyond the advertised Lite price search. <br>
Mitigation: Review the included scripts before running them, and use the Lite search script for manual Taobao and Pinduoduo searches unless broader monitoring is intended. <br>
Risk: Notification code can send price reports and searched keywords to Feishu or Telegram if credentials are configured. <br>
Mitigation: Do not add Feishu or Telegram credentials unless those destinations are approved for the price reports and keywords being processed. <br>
Risk: The package includes a ClawHub login script that is not part of the advertised price-search workflow. <br>
Mitigation: Avoid running do_login.sh unless the login flow is understood and explicitly needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/since198905/ec-price-monitor-pro) <br>
- [config.yaml](references/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text price-search reports with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manual keyword-driven searches; Lite behavior is limited to Taobao and Pinduoduo.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
