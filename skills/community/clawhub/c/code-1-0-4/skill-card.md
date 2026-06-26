## Description: <br>
Coding workflow with planning, implementation, verification, and testing for clean software development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lion504](https://clawhub.ai/user/Lion504) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to structure coding requests into planned, testable implementation steps with verification before delivery. It also provides guidance for optional local preference memory when the user explicitly asks to save coding preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional local preference memory can store sensitive information if a user asks to save secrets, credentials, or sensitive personal data. <br>
Mitigation: Do not save secrets, credentials, or sensitive personal data in ~/code/memory.md; review or delete the file when preferences should no longer be reused. <br>
Risk: Generated coding guidance or proposed changes may be incorrect or insufficiently verified. <br>
Mitigation: Review proposed changes and run the relevant tests, screenshots, or full verification workflow before delivery or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lion504/code-1-0-4) <br>
- [Skill homepage](https://clawic.com/skills/code) <br>
- [Memory setup reference](memory-template.md) <br>
- [Planning reference](planning.md) <br>
- [Execution guidance](execution.md) <br>
- [Verification reference](verification.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits, verification steps, and optional local preference-memory instructions; it does not automatically execute code or make network requests.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and artifact _meta.json; ClawHub release version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
