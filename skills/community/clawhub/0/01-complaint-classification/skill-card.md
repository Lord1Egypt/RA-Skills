## Description: <br>
Classifies user complaints under GB/T 42499-2023 and Alibaba platform rules, assigns priority and responsibility, and recommends routing for Cainiao Logistics, Cainiao Post, and Taobao Flash Purchase workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal control and complaint operations users can paste or upload complaint text, ticket IDs, or complaint batches to receive structured classification, priority, likely responsibility, and routing recommendations. The skill is intended to help triage Cainiao Logistics, Cainiao Post, and Taobao Flash Purchase complaints before final human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Complaint text may contain order numbers, names, addresses, account details, or other sensitive facts. <br>
Mitigation: Redact or replace personal and account data with placeholders unless specific details are required for classification or routing. <br>
Risk: The skill provides preliminary classification and responsibility recommendations, which may be mistaken for final adjudication. <br>
Mitigation: Route outputs to the appropriate operations, compliance, or security team for verification before taking enforcement, compensation, or customer-facing action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/01-complaint-classification) <br>
- [Judgment rules manual](artifact/RULES.md) <br>
- [Conversation examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style structured complaint classification report with priority, responsibility, routing, and remarks sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-complaint and batch-analysis outputs; sensitive complaint details should be minimized or redacted.] <br>

## Skill Version(s): <br>
1.7.0 (source: artifact/SKILL.md frontmatter; ClawHub release version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
