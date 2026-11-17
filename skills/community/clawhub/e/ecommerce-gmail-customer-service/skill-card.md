## Description: <br>
Draft-first e-commerce Gmail support that triages customer threads, verifies order and policy context, creates auditable drafts, and allows owner-controlled draft learning, memory use, and category-based automatic sending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ecom-agent-tools](https://clawhub.ai/user/ecom-agent-tools) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce merchants and support operators use this skill to process a dedicated Gmail support inbox, classify customer requests, verify product, order, storefront, and policy context, and prepare reviewable customer-service replies. It is intended for draft-first operation, with optional owner-approved learning and tightly gated automatic sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has high-authority Gmail capabilities and can create drafts, apply labels, and potentially send replies when configured. <br>
Mitigation: Use a dedicated support Gmail account, begin in draft-only mode, run acceptance tests, and enable automatic sending only after both the global setting and exact category permissions are owner-approved. <br>
Risk: Customer-service workflows may involve sensitive customer, order, payment, OAuth, or merchant-credential data. <br>
Mitigation: Keep OAuth and merchant credentials in approved secret stores only, avoid placing secrets in chat, Gmail, configuration files, user memory, reports, or the skill directory, and rely on masked reports. <br>
Risk: Long-term memory and draft-edit learning could preserve inappropriate details if used without review. <br>
Mitigation: Store only owner-approved redacted summaries, keep historical imports consent-based, periodically inspect or clear memory, and use the separate memory and learning controls. <br>
Risk: Public storefront content can be stale or inapplicable to a customer's region, order time, or channel. <br>
Mitigation: Treat public storefront discovery as candidate evidence only and verify applicability against authenticated order, policy, and merchant data before drafting or sending a response. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ecom-agent-tools/skills/ecommerce-gmail-customer-service) <br>
- [Publisher Profile](https://clawhub.ai/user/ecom-agent-tools) <br>
- [Project Homepage](https://ecomagenttools.com) <br>
- [Onboarding](references/onboarding.md) <br>
- [Gmail Operations](references/gmail-operations.md) <br>
- [Merchant Data Contract](references/merchant-data-contract.md) <br>
- [Commerce Platform API Capability and Credential Guide](references/platform-connectors.md) <br>
- [Storefront Discovery](references/storefront-discovery.md) <br>
- [Learning Workflow](references/learning-workflow.md) <br>
- [Reply Playbooks](references/reply-playbooks.md) <br>
- [Intent Taxonomy](references/intent-taxonomy.csv) <br>
- [Research Sources](references/research-sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Gmail draft text, Markdown guidance, JSON status reports, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates masked processing reports and labels Gmail threads; default behavior is draft-only unless owner-approved automatic-send gates pass.] <br>

## Skill Version(s): <br>
1.2.8 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
