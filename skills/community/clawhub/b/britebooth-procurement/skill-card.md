## Description: <br>
Read-only assistant for BriteBooth.com. Collects product IDs, templates, and lead times. Requires human execution for cart creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vismonkey19](https://clawhub.ai/user/Vismonkey19) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to research BriteBooth trade show products, artwork templates, prices, and lead-time estimates while keeping cart creation and purchase completion under direct human control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live product availability, prices, closure banners, and lead times can change after the skill retrieves them. <br>
Mitigation: Have the agent perform a fresh read-only check and ask the user to verify the final product and timeline details on BriteBooth.com before purchasing. <br>
Risk: Checkout, payment, contact, shipping, cookie, and session handling would expose sensitive user data if performed by the agent. <br>
Mitigation: Keep the skill limited to product and template links, and require the user to complete cart and checkout actions in their own browser session. <br>
Risk: Tight event deadlines can make ordinary production and proofing windows insufficient. <br>
Mitigation: Include the estimated production dates in the shopping list and direct the user to contact BriteBooth support for expedited options when the timeline is tight. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Vismonkey19/britebooth-procurement) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Vismonkey19) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown shopping list with product links, template links, prices, lead-time estimates, and status notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only output; purchase completion remains manual in the user's browser.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
