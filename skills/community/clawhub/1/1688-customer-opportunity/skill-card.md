## Description: <br>
Helps 1688 merchants inspect AI customer groups, review buyer details, activate Wangwang marketing plans, and get buyer follow-up recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External 1688 merchants use this skill to identify customer opportunities, inspect customer groups and buyer profiles, and prepare or activate follow-up outreach after merchant confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a 1688 account credential and can access customer data. <br>
Mitigation: Install only when the publisher is trusted, confirm why the credential is needed, and verify where the AK is stored before configuration. <br>
Risk: Confirmed Wangwang marketing plans can initiate customer outreach. <br>
Mitigation: Review every generated or recommended marketing message before activation and keep merchant confirmation in the workflow. <br>
Risk: Security evidence flags inconsistent credential handling and undisclosed usage reporting. <br>
Mitigation: Review credential handling and usage reporting expectations before deployment, especially for production merchant accounts. <br>


## Reference(s): <br>
- [Configure AK](artifact/references/capabilities/configure.md) <br>
- [List Customer Cluster](artifact/references/capabilities/list_customer_cluster.md) <br>
- [List Cluster Buyer Detail](artifact/references/capabilities/list_cluster_buyer_detail.md) <br>
- [List Customer Details](artifact/references/capabilities/list_customer_details.md) <br>
- [Customer Reception Advice](artifact/references/capabilities/customer_reception_advice.md) <br>
- [Customer Crowd Analysis](artifact/references/capabilities/customer_crowd_analysis.md) <br>
- [Get Cluster Marketing Plan](artifact/references/capabilities/get_cluster_marketing_plan.md) <br>
- [Activate Cluster Plan](artifact/references/capabilities/activate_cluster_plan.md) <br>
- [Interaction Specs](artifact/references/interaction-specs.md) <br>
- [Language Rules](artifact/references/lang-rules.md) <br>
- [Display Rules](artifact/references/display-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON command results with merchant-facing Markdown and interactive table or input payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some workflows require merchant confirmation before customer outreach; tool markdown is expected to be preserved verbatim.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
