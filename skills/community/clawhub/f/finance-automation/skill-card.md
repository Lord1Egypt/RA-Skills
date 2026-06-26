## Description: <br>
Automates payments, invoices, expenses, financial reports, and real-time finance notifications using Stripe, Lemon Squeezy, Telegram, email, and a Node.js API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChloePark85](https://clawhub.ai/user/ChloePark85) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and finance operators use this skill to run a finance automation service that records payment webhooks, manages invoices and expenses, and generates revenue, MRR, and profit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance-changing API routes are exposed without implemented authentication or role-based authorization. <br>
Mitigation: Add authentication and role-based authorization to all /api routes before installation or production use. <br>
Risk: Payment, customer, invoice, and notification data may include sensitive financial or personal information. <br>
Mitigation: Protect the .env file and database, use sandbox payment keys first, and review exactly what customer and payment details are sent to Telegram or email. <br>
Risk: Webhook tunnel exposure can broaden access during testing. <br>
Mitigation: Keep Stripe CLI or ngrok tunnels limited to webhook testing and disable them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ChloePark85/finance-automation) <br>
- [README.md](artifact/README.md) <br>
- [QUICKSTART.md](artifact/QUICKSTART.md) <br>
- [ARCHITECTURE.md](artifact/ARCHITECTURE.md) <br>
- [Stripe API Documentation](https://stripe.com/docs/api) <br>
- [Lemon Squeezy Documentation](https://docs.lemonsqueezy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown documentation and Node.js/SQL project files with JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an Express service, database schema, API routes, webhook handlers, setup commands, and operational documentation.] <br>

## Skill Version(s): <br>
0.2.1 (source: ClawHub release metadata; package.json lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
