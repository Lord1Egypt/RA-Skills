## Description: <br>
Provides best practices and code patterns for building, scaling, and operating production Stripe payment systems from checkout to enterprise billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, SaaS teams, founders, and marketplace builders use this skill to design, implement, audit, and operate Stripe checkout, subscription, webhook, tax, Connect, and payment monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated payment or billing changes can affect live charges, subscriptions, refunds, tax collection, or Connect payouts. <br>
Mitigation: Test in Stripe test mode first and review billing, subscription, refund, tax, and payout changes before deploying. <br>
Risk: Stripe credentials and webhook secrets are financially sensitive. <br>
Mitigation: Use restricted keys, keep live secrets out of prompts and source code, and store secrets in environment-managed configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1kalin/afrexai-stripe-production) <br>
- [Context Pack Store](https://afrexai-cto.github.io/context-packs/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript, YAML, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes checklists, scoring guidance, architecture tables, and production-readiness recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
