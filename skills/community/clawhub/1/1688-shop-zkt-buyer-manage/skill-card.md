## Description:

Helps 1688 shop operators query inquiry customers, analyze buyer purchase intent, review customer profiles, and generate Chinese follow-up scripts from authorized customer intelligence data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 shop operators and agents use this skill to review inquiry customer lists, understand purchase intent and opportunity or churn signals, inspect customer profiles, and draft follow-up messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access credentials for 1688 customer intelligence workflows.

Mitigation: Use a dedicated, least-privilege 1688 access key and avoid pasting the key into shell commands.

Risk: Credentials may be stored in local OpenClaw configuration.

Mitigation: Protect the OpenClaw configuration file and rotate any access key that may already have been written there.

Risk: The skill handles sensitive customer intelligence data and includes automatic usage reporting.

Mitigation: Install only after confirming that the deployment accepts the customer-data access and usage-reporting behavior described by the security evidence.

Risk: Gateway configuration can affect where authenticated requests are sent.

Mitigation: Verify OPENCLAW_GATEWAY_URL points only to a trusted local OpenClaw gateway before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/skills/1688-shop-zkt-buyer-manage)
- [Analyze Customer Intent](references/capabilities/analyze_customer_intent.md)
- [Configure Access Key](references/capabilities/configure.md)
- [Find Total Inquiry Customers](references/capabilities/find_total_inquiry_customers.md)
- [Get Customer Profile](references/capabilities/get_customer_profile.md)
- [Suggest Follow-up Script](references/capabilities/suggest_follow_up_script.md)
- [Usage Reporting Notes](references/skill埋点说明.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown business summaries and tables, with command JSON used by the agent to preserve structured results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-facing responses; sensitive customer amounts, counts, risk scores, and identifiers are expected to be transformed or withheld before display.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
