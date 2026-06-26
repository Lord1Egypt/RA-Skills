## Description: <br>
Choose and order food with learned preferences, price comparison, and variety protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to help an agent decide what food to order, compare delivery options, remember preferences and restrictions, and guide checkout after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate logged-in delivery apps and place real orders. <br>
Mitigation: Require explicit user confirmation before checkout and review the cart, address, total, fees, tip, and ETA before approving payment. <br>
Risk: The skill stores food preferences, allergies, household details, and order history in local files. <br>
Mitigation: Keep ~/food-delivery private, and edit or delete those files when retained preference or order-history details should be removed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/food-delivery) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with occasional shell commands and order-summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes recommendations, price comparisons, cart review summaries, confirmations, and local memory setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
