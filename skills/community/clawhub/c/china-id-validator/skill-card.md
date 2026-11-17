## Description:

Validate and extract info from Chinese ID card numbers (身份证). 身份证号码验证、归属地查询、出生日期提取、性别判断、年龄计算、15位转18位。China mainland ID card validator and parser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to validate 15- and 18-digit Chinese ID card numbers, extract province, birthdate, gender, and age fields, convert 15-digit IDs to 18-digit form, and generate clearly synthetic test numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real Chinese ID numbers are sensitive personal data and may be exposed through shared prompts, terminals, logs, or transcripts.

Mitigation: Use the skill locally, avoid entering real ID numbers in shared environments, and redact outputs before storing or sharing them.

Risk: Generated test ID numbers may look realistic and could be mistaken for real personal data.

Mitigation: Use generated IDs only for synthetic testing and label or isolate test data so it is not treated as real identity information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darbling/skills/china-id-validator)
- [Publisher profile](https://clawhub.ai/user/darbling)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON results and concise Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally; outputs validation status, extracted ID attributes, conversion results, error messages, or synthetic test IDs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
