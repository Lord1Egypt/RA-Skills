## Description:

Helps 1688 merchants inspect AI customer segments, review buyer details, generate buyer follow-up advice, monitor customer opportunities, and activate confirmed Wangwang marketing plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 merchants and sales operators use this skill to identify high-value customer segments, inspect buyer profiles, receive follow-up guidance, and launch confirmed customer outreach plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access Keys can be exposed through chat, command-line use, local files, or an untrusted gateway configuration.

Mitigation: Review the skill before installation, prefer platform-managed secret handling, avoid pasting production Access Keys unless the exposure risk is accepted, trust only approved OPENCLAW_GATEWAY_URL values, and check permissions on any openclaw.json file storing credentials.

Risk: The skill can read customer and buyer-operation data.

Mitigation: Use it only in approved merchant contexts and verify that operators have permission to access the customer data returned by the skill.

Risk: The skill can activate a Wangwang marketing plan after confirmation.

Mitigation: Require merchant review of the marketing copy and plan details before activation.

## Reference(s):

- [Configure Access Key](artifact/references/capabilities/configure.md)
- [List Customer Clusters](artifact/references/capabilities/list_customer_cluster.md)
- [List Cluster Buyer Detail](artifact/references/capabilities/list_cluster_buyer_detail.md)
- [Customer Reception Advice](artifact/references/capabilities/customer_reception_advice.md)
- [Customer Crowd Analysis](artifact/references/capabilities/customer_crowd_analysis.md)
- [Get Cluster Marketing Plan](artifact/references/capabilities/get_cluster_marketing_plan.md)
- [Activate Cluster Plan](artifact/references/capabilities/activate_cluster_plan.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured JSON returned by local CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language merchant-facing responses; may include tables, buyer profiles, follow-up suggestions, and CRM links.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
