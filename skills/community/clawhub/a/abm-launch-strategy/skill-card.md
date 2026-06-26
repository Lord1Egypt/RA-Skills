## Description: <br>
Helps users plan SaaS product launches, feature announcements, and release strategies using phased launch planning, ORB channel strategy, Product Hunt guidance, and post-launch follow-through. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams and employees use this skill to plan product launches, feature announcements, Product Hunt campaigns, early-access programs, and post-launch recovery or follow-up plans. It tailors recommendations to available product marketing context when present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use local product marketing context files if they are present, which can expose confidential launch, market, customer, or strategy details to the agent response. <br>
Mitigation: Before installing or invoking the skill, review `.agents/product-marketing-context.md` and `.claude/product-marketing-context.md` and remove secrets or unrelated confidential information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariokarras/abm-launch-strategy) <br>
- [Publisher profile](https://clawhub.ai/user/mariokarras) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, markdown] <br>
**Output Format:** [Markdown guidance with launch plans, checklists, channel recommendations, and tactical next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local product marketing context if present before asking follow-up questions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
