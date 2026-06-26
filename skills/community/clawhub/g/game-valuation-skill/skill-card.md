## Description: <br>
Game Account Valuation helps agents estimate the value of a specific supported game account for Wangzhe Rongyao, Peacekeeper Elite, or Delta Force. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-lin](https://clawhub.ai/user/arc-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when a user asks what a specific supported game account is worth. It is not intended for market trend, listing-data, price-distribution, or account market analysis requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags that account-linked data and QR-login workflow data may be sent to a remote valuation service over plain HTTP with limited consent or privacy disclosure. <br>
Mitigation: Review before installing, inform users before sending account identifiers or QR-login workflow data, and prefer an HTTPS-backed version with clear retention and privacy handling. <br>
Risk: QR-login files and raw debug commands can expose account workflow data during valuation. <br>
Mitigation: Use a private temporary QR-code directory, remove or restrict generated QR artifacts after use, and reserve raw debug commands for troubleshooting by trusted operators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arc-lin/game-valuation-skill) <br>
- [YY Youcang marketplace](https://mall.yy.com/?pageId=20000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style valuation report with shell command execution guidance and service response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include valuation amount, price range, core account attributes, QR-login status, and a link to a detailed valuation page.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
