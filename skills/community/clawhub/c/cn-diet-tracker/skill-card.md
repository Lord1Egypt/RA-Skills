## Description:

Cn Diet Tracker helps agents record Chinese-language meal entries, track daily and weekly calories, manage calorie targets, and summarize local diet logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain a Chinese-language food diary, estimate calorie intake, review weekly totals, and manage a daily calorie target through a local CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Food logs can contain sensitive personal health or lifestyle data stored on the local filesystem.

Mitigation: Protect or remove ~/.qclaw/workspace/diet.json on shared systems and avoid entering sensitive notes that do not need to be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-diet-tracker)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores meal, calorie, category, note, and target data locally at ~/.qclaw/workspace/diet.json.]

## Skill Version(s):

1.2.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
