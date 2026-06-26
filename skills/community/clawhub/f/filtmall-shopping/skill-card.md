## Description: <br>
Use this skill when a user wants to browse, compare, buy, pay for, query orders, track logistics, manage addresses, cancel or refund eligible orders, or apply after-sale service on Filtalgo through the bundled Agent Tool Gateway CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[filtmall](https://clawhub.ai/user/filtmall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to search products, manage carts and addresses, start checkout and wallet payment, review orders, track logistics, cancel or refund eligible orders, and request supported after-sale service through Filtalgo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect purchases, payments, orders, refunds, after-sale requests, and saved addresses. <br>
Mitigation: Review cart, checkout, payment, address, cancellation, refund, and after-sale actions with the user before execution. <br>
Risk: Broad implicit activation can make ambiguous shopping prompts more likely to trigger account-affecting actions. <br>
Mitigation: Avoid ambiguous shopping prompts and confirm product, quantity, address, order, and refund details before using commands that change state. <br>
Risk: The bundled remote-dev OAuth client details are public configuration rather than private credentials. <br>
Mitigation: Do not print access tokens, refresh tokens, client secrets, or OAuth bootstrap secrets in user-facing output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/filtmall/filtmall-shopping) <br>
- [FiltMall publisher profile](https://clawhub.ai/user/filtmall) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON CLI output references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and authenticated Filtalgo account access; user-facing output should not expose access tokens, refresh tokens, client secrets, or OAuth bootstrap secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
