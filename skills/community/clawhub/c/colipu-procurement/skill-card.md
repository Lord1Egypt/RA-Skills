## Description: <br>
A Colipu B2B office procurement assistant that helps agents search products, prepare and place orders, query order details, and cancel eligible orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simsq](https://clawhub.ai/user/simsq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and procurement operators use this skill through an agent to search Colipu office supplies, prepare or place orders after explicit confirmation, and query or cancel orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place or cancel real Colipu orders without the final confirmation promised by the documentation. <br>
Mitigation: Require a visible final summary and explicit per-action user confirmation before invoking colipu_order.py, colipu_search.place_order, quick_order, or cancel_order. <br>
Risk: The skill requires Colipu account credentials and session cookies for API access. <br>
Mitigation: Use a least-privileged Colipu account and keep credentials in environment variables or secret storage instead of code, logs, or public documentation. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/simsq/colipu-procurement) <br>
- [Configuration guide](artifact/CONFIG.md) <br>
- [Colipu API reference](artifact/references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Colipu credentials in environment variables or secret storage; order and cancellation actions should include a visible final summary and explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
