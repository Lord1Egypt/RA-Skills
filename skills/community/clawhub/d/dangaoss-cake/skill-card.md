## Description: <br>
Helps users order cakes, desserts, snacks, and flowers from dangaoss.com by managing delivery addresses, searching products, generating order links, and checking order status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhang1058](https://clawhub.ai/user/zhang1058) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to place dangaoss.com orders for cakes, desserts, snacks, or flowers through an agent-assisted flow. It supports address selection, product search, order-link generation, and order-status lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles dangaoss.com account tokens and delivery details. <br>
Mitigation: Use only with explicit user-provided tokens, treat dgss_token.md as sensitive, and clear stored token or address data when finished. <br>
Risk: The skill can run local commands and perform account-changing ordering actions. <br>
Mitigation: Require approval before command execution or actions that add addresses, generate order links, or otherwise affect the user's account. <br>
Risk: Plaintext local storage can leak tokens or delivery details if committed or synced. <br>
Mitigation: Keep dgss_token.md out of version control and avoid syncing it to shared storage. <br>


## Reference(s): <br>
- [蛋叔商城 API 接口文档](references/api_docs.md) <br>
- [ClawHub release page](https://clawhub.ai/zhang1058/dangaoss-cake) <br>
- [Publisher profile](https://clawhub.ai/user/zhang1058) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown responses with product tables, order links, command invocations, and JSON-derived status summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local plaintext token and delivery-address state during the ordering workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
