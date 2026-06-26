## Description: <br>
Organizes sales-to-delivery customer information into a structured handoff package and identifies promise risks, implementation prerequisites, and items that need confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer success, sales, and implementation teams use this skill to turn opportunity notes, commitments, and customer context into a review-ready handoff brief with promised items, prerequisites, risks, questions, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer handoff inputs may contain personal, confidential, contractual, or commercially sensitive information. <br>
Mitigation: Use only intended local handoff materials, minimize or redact sensitive data where practical, and review the draft before sharing. <br>
Risk: The generated brief could omit context or misstate a commitment if the source notes are incomplete. <br>
Mitigation: Treat the output as a review draft and resolve the explicit confirmation items before execution, sending, or system changes. <br>
Risk: The local helper can write an output file to a user-selected path. <br>
Mitigation: Choose output paths deliberately, use dry-run or stdout when appropriate, and avoid writing over important files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/account-handoff-builder) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Structured Output Specification](artifact/resources/spec.json) <br>
- [Output Template](artifact/resources/template.md) <br>
- [Smoke Test](artifact/tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown handoff brief; optional JSON wrapper from the local Python helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print to stdout or write a local output file; uses python3 and the Python standard library only.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
