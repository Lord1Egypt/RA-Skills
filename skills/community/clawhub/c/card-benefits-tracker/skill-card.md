## Description: <br>
Track and maximize credit card benefits (monthly, quarterly, yearly). Manage cards, log benefit usage, get reminders for expiring perks, see ROI summaries, and optimize spending categories for maximum rewards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[softtrymee](https://clawhub.ai/user/softtrymee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to track credit-card perks, log monthly, quarterly, and yearly benefit usage, receive reminders for expiring credits, review annual-fee ROI, and compare spending categories across tracked cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores card names, annual fees, membership dates, benefit details, and usage history in local JSON files. <br>
Mitigation: Install only if local storage of this financial-planning data is acceptable, and do not store card numbers, bank logins, API keys, or other secrets in the tracker. <br>
Risk: Optional web lookups can send card names, benefit questions, or spending categories to a search provider. <br>
Mitigation: Approve web lookups only when that disclosure is acceptable, and verify discovered benefit details against issuer sources before saving updates. <br>
Risk: ROI and spending-category recommendations can be wrong when issuer benefits, cashback rates, or user-entered data are outdated. <br>
Mitigation: Treat recommendations as planning guidance and confirm current issuer terms before changing cards, benefits, or spending behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/softtrymee/card-benefits-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summaries with tables, JSON command results, and CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON files for card catalogs and period tracking; web lookups are optional and should be confirmed before saving benefit or rewards data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
