## Description:

Generates Douyin video title ideas in multiple styles to help creators improve audience attention, views, and engagement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyq56565656](https://clawhub.ai/user/yyq56565656)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, social media operators, and brand marketing teams use this skill to draft Douyin title options for a topic and compare style-specific estimated performance signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PowerShell wrapper can turn crafted title inputs into local command execution.

Mitigation: Prefer running the Python script directly with trusted inputs, or replace Invoke-Expression with argument-array process invocation before accepting untrusted text.

Risk: Generated performance estimates may be mistaken for guaranteed platform outcomes.

Mitigation: Review titles before publishing and treat estimated views, engagement, and recommendation weight as illustrative signals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yyq56565656/skills/douyin-title-generator-v2)
- [README](artifact/README.md)
- [Product overview](artifact/产品介绍.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files]

**Output Format:** [Markdown-like text report with generated titles and estimated views, engagement, and recommendation weight; optional exported text file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Randomized title selection; direct Python use requires no additional package dependencies.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
