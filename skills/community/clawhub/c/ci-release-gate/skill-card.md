## Description: <br>
CI release engineer skill for validation gating, release-readiness checks, and automation-safe delivery criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to assess CI coverage, merge gates, release readiness, repeatable validation evidence, and blockers before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A release-gate recommendation could be mistaken for actual approval to merge, release, notify, or change CI configuration. <br>
Mitigation: Treat the output as advisory and require explicit user approval before taking delivery or configuration actions. <br>
Risk: The skill includes project-specific Weline validation rules and an escalation role that may not fit every environment. <br>
Mitigation: Confirm the referenced Weline documents, dedicated-instance rules, default-port restriction, and named escalation role before adoption. <br>
Risk: Weak, flaky, or non-repeatable validation evidence can lead to an incorrect release-readiness conclusion. <br>
Mitigation: Require repeatable CI-compatible evidence for mandatory gates and report missing or flaky prerequisites as blockers. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Release-gate recommendation with satisfied checks, missing gates, blockers, environment risks, follow-up actions, and collaboration status.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
