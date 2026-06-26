## Description: <br>
Cash App Pay integration skill that helps agents guide developers through Cash App Pay APIs, SDKs, sandbox testing, webhooks, and dispute handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and payment integration teams use this skill to plan and implement Cash App Pay for merchant or payment-service-provider integrations, including customer authorization, payment creation, sandbox testing, webhooks, refunds, and disputes. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through real payment, refund, capture, void, dispute, webhook, and API-key operations. <br>
Mitigation: Use sandbox credentials first and require explicit human approval before any production payment, refund, capture, void, dispute, webhook, or key-management action. <br>
Risk: Cash App API credentials could be overexposed or used beyond the intended integration scope. <br>
Mitigation: Keep credentials server-side, use least-privilege scoped keys, set merchant and amount limits, and rotate or revoke credentials after use. <br>
Risk: Repeated write requests may create duplicate charges, refunds, or merchant records if idempotency is mishandled. <br>
Mitigation: Require a unique idempotency key for each write operation and review generated request bodies before execution. <br>
Risk: Cash App Pay availability is limited to U.S. merchants and customers. <br>
Mitigation: Confirm merchant, customer, and currency eligibility before using the guidance for a production integration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codejika/cashapp) <br>
- [Cash App Developer Documentation](https://developers.cash.app) <br>
- [Cash App API base](https://api.cash.app) <br>
- [Cash App sandbox API base](https://sandbox.api.cash.app) <br>
- [Cash App Pay Partner API documentation](https://developers.cash.app/cash-app-pay-partner-api/guides/welcome) <br>
- [Cash App Network API reference](https://developers.cash.app/cash-app-pay-partner-api/api-reference/network-api/list-brands) <br>
- [Pay Kit Web guide](https://developers.cash.app/cash-app-pay-partner-api/guides/pay-kit-sdk/pay-kit-web-overview/getting-started) <br>
- [Pay Kit iOS guide](https://developers.cash.app/cash-app-pay-partner-api/guides/pay-kit-sdk/pay-kit-i-os) <br>
- [Pay Kit Android guide](https://developers.cash.app/cash-app-pay-partner-api/guides/pay-kit-sdk/pay-kit-android) <br>
- [Cash App API request signing guidance](https://developers.cash.app/cash-app-pay-partner-api/guides/technical-guides/api-fundamentals/requests/making-requests) <br>
- [Cash App Postman collection](https://developers.cash.app/cash-app-pay-partner-api/guides/technical-guides/sandbox/postman-collection) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API endpoint tables and bash curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CASHAPP_CLIENT_ID and CASHAPP_API_KEY when used against Cash App APIs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
