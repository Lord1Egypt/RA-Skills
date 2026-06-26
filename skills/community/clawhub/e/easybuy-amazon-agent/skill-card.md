## Description: <br>
Tracks Amazon prices, monitors orders, scrapes reviews, fetches order details, drafts refund messages, and manages refund cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Amazon shoppers and browser agents use this skillpack to inspect orders and products, monitor prices, collect evidence, and prepare refund, replacement, return, or after-sales messages. It is intended for live Amazon sessions where the user can review proposed browser actions before approving them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The assistant gives an AI-planned browser agent broad access to inspect and act on webpages beyond the Amazon-focused purpose. <br>
Mitigation: Use it only on intended Amazon pages, inspect each confirmation carefully, and approve only actions that match the current shopping task. <br>
Risk: Configured model endpoints and API keys can affect where order, product, page, or message context is sent. <br>
Mitigation: Verify the configured endpoint before use and use a dedicated low-privilege AI API key. <br>
Risk: Evidence packages, screenshots, DOM snippets, and message drafts can include sensitive order or account information. <br>
Mitigation: Clear extension storage and exported artifacts after handling sensitive orders or messages. <br>
Risk: Automated message entry or sending can submit incorrect after-sales messages if used without review. <br>
Mitigation: Avoid enabling auto-send and review every drafted message before approving any send-related action. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/luoqianchenguni-max/easybuy-amazon-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON skill outputs, browser action results, drafted text, exported evidence artifacts, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Chrome MV3, Amazon login for live flows, browser permissions, and user review of confirmations before sensitive actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skills/registry.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
