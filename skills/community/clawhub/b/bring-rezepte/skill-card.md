## Description: <br>
Bring Rezepte helps an agent search recipe ideas, parse recipe URLs for ingredients, and add confirmed ingredients to a Bring shopping list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dolverin](https://clawhub.ai/user/Dolverin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and household shoppers use this skill to find German-language recipe ideas, inspect ingredients, and update Bring shopping lists after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill receives access to a Bring account and shopping lists. <br>
Mitigation: Provide Bring credentials through secure environment or secret storage, and install only when that account access is acceptable. <br>
Risk: A user-supplied content URL can receive Bring authorization headers. <br>
Mitigation: Use only trusted official Bring API content URLs with --content-url. <br>
Risk: A custom BRING_NODE_API_PATH can load local code in the agent runtime. <br>
Mitigation: Leave BRING_NODE_API_PATH unset unless it points to reviewed local code. <br>


## Reference(s): <br>
- [Bring Inspirations API Reference](references/bring-inspirations.md) <br>
- [ClawHub skill page](https://clawhub.ai/Dolverin/bring-rezepte) <br>
- [Publisher profile](https://clawhub.ai/user/Dolverin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and Bring credentials; writes to Bring lists only after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
