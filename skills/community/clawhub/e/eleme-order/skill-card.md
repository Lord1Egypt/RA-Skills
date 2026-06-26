## Description: <br>
Order food, drinks, or groceries from Ele.me (饿了么) by using Playwright browser automation to browse restaurants, add items to cart, and pause for user confirmation and manual payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xbralready](https://clawhub.ai/user/Xbralready) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to have an agent navigate Ele.me, choose restaurants and items, prepare a food, drink, or grocery order, and pause for user confirmation before order submission and manual payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent controls a real browser session on Ele.me and may view delivery details while preparing an order. <br>
Mitigation: Install only when this access is acceptable, and review the final address, items, and total before confirming. <br>
Risk: The skill can prepare an order that affects real-world purchases. <br>
Mitigation: Require user confirmation on the order page before submission and complete payment manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xbralready/eleme-order) <br>
- [Ele.me H5](https://h5.ele.me) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with browser automation actions and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and a Playwright MCP server; the user confirms order details and completes payment manually.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
