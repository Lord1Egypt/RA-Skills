## Description:

FitDietKernel is a personal diet knowledge base that helps an AI assistant calculate carbohydrate targets, food equivalents, meal logs, and weekly diet reports for carbon cycling, ketogenic, bulking, and cutting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yibinpro](https://clawhub.ai/user/yibinpro)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to give an AI assistant a local fitness diet profile, food registry, macro rules, and logging workflow so it can calculate daily carbohydrate budgets, food equivalents, meal status, and weekly summaries. It is aimed at personal AI-assisted tracking for carbon cycling, ketogenic, bulking, cutting, and intermittent fasting routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal health, weight, diet, and log data in local JSON and Markdown files.

Mitigation: Grant the agent access only to the FitDietKernel directory, review profile and log contents for sensitive data, and provide a clear way to delete local weight and diet history.

Risk: The HTML desktop app loads Chart.js from an unpinned external CDN URL.

Mitigation: Use a bundled or pinned Chart.js build with integrity checks before relying on the desktop HTML interface.

Risk: The skill workflow can modify food_registry.json and log files.

Mitigation: Require user confirmation before food registry or log writes, and review generated changes before treating them as durable records.

Risk: Installer or app commands may be run with broader privileges than the skill needs.

Mitigation: Pin the ClawHub installer version, avoid administrator or root execution, and keep the working directory scoped to the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yibinpro/skills/fitdietkernel)
- [ClawHub Publisher Profile](https://clawhub.ai/user/yibinpro)
- [Artifact README](README.md)
- [Skill Definition](SKILL.md)
- [Carbon Cycling Rules](knowledge_base/rules.md)
- [Food Registry](knowledge_base/food_registry.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and Markdown file updates, optional shell commands, and local report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local profile, food registry, diet log, and weekly report files when the user grants access and confirms writes.]

## Skill Version(s):

1.0.1 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
