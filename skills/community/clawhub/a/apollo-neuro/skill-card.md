## Description:

像神经系统一样选择最快路径：紧急的事快速处理，复杂的事慢慢想。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users use Apollo Neuro to classify incoming tasks into fast, standard, delayed, or deeper-analysis response paths based on urgency, complexity, and available circadian state. The skill helps an agent choose a routing recommendation and produce a concise routing report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence task-routing policy and may reduce confirmations or validation.

Mitigation: Use it only where external confirmation and validation requirements remain enforced outside the skill.

Risk: The shell script can store raw task text in route-state JSON.

Mitigation: Avoid using it for workflows that handle secrets or sensitive user content unless that state file is protected and retention is acceptable.

Risk: The security verdict is suspicious because of broad behavior changes.

Mitigation: Review and scan the skill before deployment, especially before using it in workflows that send messages, modify files, publish content, or spend money.

## Reference(s):

- [Apollo Neuro Skill Page](https://clawhub.ai/nic-yuan/skills/apollo-neuro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text and shell-script routing reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write route-state JSON containing raw task text when the bundled shell script is used.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
