## Description: <br>
Look up credit card rewards eligibility for merchants by checking MCC codes and card bonus categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gibtang](https://clawhub.ai/user/gibtang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to identify a merchant's MCC and compare credit card bonus eligibility, rewards rates, spend caps, and exclusions before choosing a card. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Merchant, domain, or MCC lookup queries are sent to check-mcc.com. <br>
Mitigation: Avoid entering unnecessary personal transaction details or sensitive account information in lookup queries. <br>
Risk: Rewards recommendations may be incomplete or outdated. <br>
Mitigation: Verify important rewards decisions, exclusions, and spend caps with the card issuer before acting. <br>


## Reference(s): <br>
- [CheckMCC API base URL](https://check-mcc.com) <br>
- [ClawHub CheckMCC listing](https://clawhub.ai/gibtang/check-mcc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary of MCC, merchant category, eligible cards, rewards rates, spend caps, conditions, and lookup errors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include card eligibility details returned by the CheckMCC API for SG or US regions.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
