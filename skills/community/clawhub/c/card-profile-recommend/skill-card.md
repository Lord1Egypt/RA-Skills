## Description: <br>
Analyzes a multi-card credit-card portfolio, grades each card, recommends 2-3 new additions with signup-bonus strategy, checks issuer rules, and sequences applications across major U.S. issuers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahongc](https://clawhub.ai/user/jiahongc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal-finance researchers use this skill to audit current credit-card portfolios, identify weak or overlapping cards, and plan new personal-card applications under issuer eligibility rules. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Credit-card offers, fees, rewards, issuer rules, and eligibility terms can change or be misread. <br>
Mitigation: Verify current issuer terms, fees, offers, eligibility rules, and secondary research before acting on recommendations. <br>
Risk: The skill may request or process sensitive financial context while researching card recommendations. <br>
Mitigation: Do not provide card numbers, Social Security numbers, banking logins, wallet credentials, or other secrets; only provide BRAVE_API_KEY when comfortable using it for search queries. <br>
Risk: Recommendations may influence financial decisions but are generated as research assistance. <br>
Mitigation: Treat outputs as financial research, review assumptions and confidence notes, and make final decisions independently. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/jiahongc/card-profile-recommend) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables, numbered lists, sourced links, and occasional shell command examples for optional Brave Search use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask clarifying questions for ambiguous cards; uses web search/fetch and optional BRAVE_API_KEY for current card terms.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
