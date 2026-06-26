## Description: <br>
Buy and return items on Amazon using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to guide an agent through Amazon order history searches, reorders, new purchases, and return submissions in a browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent control over credentials, purchases, and returns without enough user confirmation. <br>
Mitigation: Require manual login and explicit approval before every order or return submission, including item, price or refund, address, payment or refund method, return reason, condition answers, and drop-off details. <br>
Risk: A persistent browser profile may retain Amazon account access after use. <br>
Mitigation: Use a dedicated browser profile and log out or clear the profile when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BrennerSpear/amazon-ordering) <br>
- [Publisher profile](https://clawhub.ai/user/BrennerSpear) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and browser workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in browser profile, agent-browser CLI, Chrome DevTools Protocol access, and user verification of purchase and return details.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
