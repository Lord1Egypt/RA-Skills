## Description: <br>
Standardizes evidence anchors so agents can record, verify, trace, and reuse project memory evidence with explicit confidence levels and review criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangwill2023](https://clawhub.ai/user/jiangwill2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and agents use this skill to classify project evidence as direct, indirect, or referenced evidence, then write evidence anchors that support memory records, handoffs, reviews, and project status claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evidence anchors can include sensitive paths, URLs, logs, financial records, or signed documents. <br>
Mitigation: Keep access-controlled evidence private, redact unnecessary sensitive details, and preserve only the minimum path or reference needed for verification. <br>
Risk: Stale evidence can cause project memory to overstate current status. <br>
Mitigation: Use the skill's periodic review workflow to re-check URLs, files, configuration, and logs every one to three months. <br>
Risk: Weak referenced evidence can be mistaken for completion proof. <br>
Mitigation: Require Level 1 direct evidence for DONE claims and downgrade unsupported claims to PARTIAL or BLOCKED until stronger evidence exists. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangwill2023/evidence-anchor) <br>
- [Publisher profile](https://clawhub.ai/user/jiangwill2023) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Templates] <br>
**Output Format:** [Markdown guidance with structured evidence-anchor templates and review criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are concise evidence classifications, acceptance checks, status mappings, and reusable Markdown snippets.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
