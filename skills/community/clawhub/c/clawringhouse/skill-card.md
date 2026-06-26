## Description: <br>
Helps agents research products with Clawringhouse, compare options, prepare carts or affiliate-tagged product links, and present purchase-ready recommendations for human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[francoisjosephlacroix](https://clawhub.ai/user/francoisjosephlacroix) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and their agents use this skill to research gifts or household supplies, compare options, prepare shopping carts, and send budget-conscious recommendations for human review before purchase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries are sent to Clawringhouse. <br>
Mitigation: Tell the user when a shopping query will be sent to Clawringhouse and avoid including sensitive personal details unless the user approves. <br>
Risk: The skill encourages use of memory, calendar context, and logged-in browser sessions for proactive shopping. <br>
Mitigation: Ask before reading memory or calendar context, opening a logged-in shopping session, or using browser automation on a user's shopping account. <br>
Risk: Cart automation can add or change items before the user has reviewed them. <br>
Mitigation: Require explicit user approval before adding or changing cart items, and stop at cart preparation rather than checkout. <br>
Risk: Affiliate-tagged Amazon links may set tracking cookies or attribution. <br>
Mitigation: Disclose affiliate-tagged links before using them and ask before setting affiliate links or cookies. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/francoisjosephlacroix/clawringhouse) <br>
- [Clawringhouse API](https://clawringhouse.onrender.com) <br>
- [Clawringhouse Website](https://clawringhouse.shop) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples, API URLs, cart links, and product-link recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations may include affiliate-tagged Amazon links and cart URLs for human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
