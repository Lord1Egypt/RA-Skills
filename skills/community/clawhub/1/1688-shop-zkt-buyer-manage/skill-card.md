## Description: <br>
Helps authorized 1688 shop operators query inquiry customers, analyze buyer intent, generate follow-up scripts, and produce customer profile summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External 1688 shop operators and their authorized agents use this skill to manage inquiry customers, identify buyer intent or churn risk, and draft follow-up guidance from account data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles 1688 account credentials and detailed customer data. <br>
Mitigation: Install and run it only when authorized to use the relevant 1688 account and customer data; treat AK values, buyer identifiers, customer profiles, and purchase metrics as sensitive. <br>
Risk: Local credential persistence and automatic usage reporting may be unacceptable in some environments. <br>
Mitigation: Review credential storage and telemetry behavior before deployment, and use the skill only where those practices are approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1688aiinfra/1688-shop-zkt-buyer-manage) <br>
- [Analyze Customer Intent capability reference](references/capabilities/analyze_customer_intent.md) <br>
- [Configure capability reference](references/capabilities/configure.md) <br>
- [Find Total Inquiry Customers capability reference](references/capabilities/find_total_inquiry_customers.md) <br>
- [Get Customer Profile capability reference](references/capabilities/get_customer_profile.md) <br>
- [Suggest Follow-Up Script capability reference](references/capabilities/suggest_follow_up_script.md) <br>
- [Skill usage reporting notes](references/skill埋点说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with structured tables and Chinese-language business guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authorized 1688 access key credentials and may query customer profiles, buyer identifiers, and purchase metrics.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
