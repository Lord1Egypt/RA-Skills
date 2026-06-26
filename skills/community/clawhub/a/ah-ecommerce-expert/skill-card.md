## Description: <br>
Provides e-commerce platform guidance across online retail architecture, checkout, payments, inventory, fulfillment, customer experience, and conversion optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and operators use this skill to plan and implement e-commerce platforms, shopping carts, checkout flows, product catalogs, inventory workflows, order fulfillment, and customer experience improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated e-commerce examples may affect sensitive store operations such as charges, refunds, fulfillment, inventory changes, or customer data handling if copied into production systems. <br>
Mitigation: Use sandbox payment credentials first, scope service credentials tightly, add authentication and authorization checks, verify webhooks, avoid logging secrets or payment data, and require explicit human approval for real charges, refunds, fulfillment, inventory changes, and customer-data changes. <br>
Risk: Payment-processing and customer-data workflows can create compliance and security exposure when adapted without review. <br>
Mitigation: Review implementations for PCI DSS expectations, secure session management, input validation, rate limiting, webhook verification, and data-protection controls before deployment. <br>


## Reference(s): <br>
- [Ecommerce Expert code examples](references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/mtsatryan/ah-ecommerce-expert) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mtsatryan) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with code examples and implementation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples may reference payment, search, cloud, database, and fulfillment integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
