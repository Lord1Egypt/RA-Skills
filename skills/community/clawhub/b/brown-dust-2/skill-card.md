## Description: <br>
Automates Brown Dust 2 daily, weekly, and event attendance check-ins plus gift-code discovery and redemption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XiaoYiWeio](https://clawhub.ai/user/XiaoYiWeio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Brown Dust 2 players use this skill to run account check-ins, inspect current events, fetch available gift codes, and redeem rewards through local scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a reusable Brown Dust 2 web-shop access token for future sign-in actions. <br>
Mitigation: Use only on a trusted local device, keep the token out of chat and screenshots, and delete the saved .token file after use or on shared devices. <br>
Risk: The skill can perform account actions such as check-ins and gift-code redemption through API calls. <br>
Mitigation: Confirm each sign-in or redemption run before execution and review script output for failed, expired, or already-used actions. <br>
Risk: Gift-code redemption uses a saved or provided in-game nickname. <br>
Mitigation: Verify the nickname before redemption and remove the saved .nickname file if the device or workspace is shared. <br>


## Reference(s): <br>
- [Brown Dust 2 ClawHub listing](https://clawhub.ai/XiaoYiWeio/brown-dust-2) <br>
- [BD2 Web Shop](https://webshop.browndust2.global/CT/) <br>
- [BD2Pulse](https://thebd2pulse.com) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Python scripts that call Brown Dust 2 web-shop, event, coupon, and BD2Pulse endpoints.] <br>

## Skill Version(s): <br>
1.1.1 (source: evidence.release.version and package.json; SKILL.md frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
