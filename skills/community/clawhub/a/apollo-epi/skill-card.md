## Description: <br>
Apollo Epi helps an agent preserve learned preferences, recurring patterns, and experience summaries so future sessions do not have to start from scratch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an agent identify learned preferences or repeated task patterns, choose a persistence layer such as memory, fine-tuning data, or a follow-on skill, and check whether knowledge-transfer records are present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to preserve learned information across sessions with broad triggers and weak consent boundaries. <br>
Mitigation: Require explicit user confirmation before writing to MEMORY.md, fine-tuning data, or a new skill. <br>
Risk: Cross-session learning records may accidentally retain secrets, credentials, sensitive personal data, or unreviewed operational details. <br>
Mitigation: Review and redact retained content before persistence, and avoid storing sensitive data in learning or memory artifacts. <br>


## Reference(s): <br>
- [Apollo Epi on ClawHub](https://clawhub.ai/nic-yuan/apollo-epi) <br>
- [nic-yuan publisher profile](https://clawhub.ai/user/nic-yuan) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize memory and learning-state checks for agent review.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
