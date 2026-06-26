## Description: <br>
Generates professional, evidence-grounded responses to refund disputes and customer complaints that protect the seller while preserving buyer relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ecommerce sellers, support teams, and marketplace operators use this skill to assess refund disputes, organize evidence, choose a resolution strategy, and draft separate platform submissions and buyer messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Buyer records, chat logs, tracking data, payment evidence, photos, and dispute history can contain sensitive personal or commercial information. <br>
Mitigation: Collect only the evidence needed for the specific dispute, keep logs access-controlled and time-limited, and avoid including unnecessary buyer data in generated responses. <br>
Risk: Marketplace and payment-processor dispute procedures can change, so stale policy references may weaken a response or miss a deadline. <br>
Mitigation: Verify current platform and processor policies in the seller center before submission, record absolute deadlines with time zones, and submit before the final response window. <br>
Risk: Block-list or fraud-pattern recommendations can unfairly affect buyers if applied without objective support. <br>
Mitigation: Require objective evidence and human review before permanent or automated buyer blocking, and document the reason for any prevention action. <br>
Risk: A draft may cite evidence that the seller does not actually have or cannot attach. <br>
Mitigation: Inventory evidence before drafting, attach or precisely reference every cited artifact, and disclose or remove any unsupported claim. <br>


## Reference(s): <br>
- [Dispute Resolver on ClawHub](https://clawhub.ai/leooooooow/dispute-resolver) <br>
- [Dispute Resolver - Output Template](references/output-template.md) <br>
- [Resolution Decision Matrix](references/resolution-decision-matrix.md) <br>
- [Platform Rules & Evidence Standards](references/platform-rules.md) <br>
- [Response Templates & Tone Calibration](references/response-templates.md) <br>
- [Dispute Response Quality Checklist](assets/dispute-response-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown response package with case assessment, platform/evidence submission, buyer message, and prevention log guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided dispute facts and evidence; does not create evidence or verify current platform rules.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
