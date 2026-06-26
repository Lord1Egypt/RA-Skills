## Description: <br>
Daily Hot Deals generates concise daily hot-deal reports from deal data for savings-focused users and resale opportunity review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[275254cl-hash](https://clawhub.ai/user/275254cl-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to generate daily summaries of notable product discounts, grouped by category with pricing details and deal timing. The included artifact currently provides a local Python report generator rather than live aggregation or delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation advertises WeChat delivery, paid subscriptions, live deal aggregation, and scheduled push behavior that are not implemented in the included artifact. <br>
Mitigation: Treat the current release as a local report generator and verify any future delivery, subscription, aggregation, or scheduling feature before enabling it. <br>
Risk: Future push or delivery features could transmit account identifiers or report data without clear user expectations. <br>
Mitigation: Before enabling delivery, confirm what data is sent, when it is sent, and how users can disable the behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/275254cl-hash/daily-hot-deals) <br>
- [Publisher profile](https://clawhub.ai/user/275254cl-hash) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text report with Markdown-style sections and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 for the included local report generator.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
