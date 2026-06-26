## Description: <br>
Automates Anjuke account operations for login, listing publication, listing checks, description optimization, incremental promotion, and government verification workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuapi2020](https://clawhub.ai/user/chuapi2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Real-estate operators and agents use this skill to run browser-based Anjuke account workflows, including login, checking available listing capacity, publishing listings, and improving low-performing listing descriptions. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store passwords, names, or identity-check fragments in skill files. <br>
Mitigation: Use interactive login, an existing platform session, or an approved secret store instead of saving credentials or identity details in skill documents. <br>
Risk: The skill can publish, transfer, or edit real-estate listings without clear approval gates. <br>
Mitigation: Require explicit human review and confirmation before publishing listings, transferring internal listing data to Anjuke, or saving live listing edits. <br>
Risk: Generated listing descriptions could include incorrect or unsupported property claims. <br>
Mitigation: Require generated descriptions to use only verified property and seller information before they are saved or published. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chuapi2020/anjuke-skill) <br>
- [Account login reference](references/login_your_account.md) <br>
- [Description optimization reference](references/optimize_description.md) <br>
- [Listing publication reference](references/publish_house.md) <br>
- [Internal listing push reference](references/push_house.md) <br>
- [Anjuke login portal](https://vip.anjuke.com/portal/login) <br>
- [Anjuke listing management](https://vip.anjuke.com/threenets/mix/second-hand/list__sl) <br>
- [Anjuke broker delivery advice](https://ai.anjuke.com/broker/consult/delivery-advice) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown or plain text instructions for browser-based account and listing workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated real-estate listing copy, account workflow status, and confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
