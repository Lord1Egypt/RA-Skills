## Description:

FitBuddy is a fitness and diet tracking assistant that helps an agent record meals, weight, exercise, and hydration; calculate BMR, TDEE, calories, and macros; generate progress reports and charts; and manage reminder-driven check-ins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[promisewhh](https://clawhub.ai/user/promisewhh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and individuals use FitBuddy through an agent to track nutrition, body weight, exercise, hydration, and fitness progress. The skill supports setup, daily logging, macro-aware recommendations, reminders, and weekly or monthly reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive fitness and health information locally.

Mitigation: Review the stored profile and records before use, restrict filesystem access to the intended fitbuddy-data directory, and avoid sharing those files unnecessarily.

Risk: Persistent reminders and configured messaging channels may expose reminder content or continue running longer than intended.

Mitigation: Review reminder schedules and channel configuration during setup, disable unneeded reminders, and limit message content sent through external channels.

Risk: The documented device approval flow can approve the latest pending device without confirming its identity.

Mitigation: Verify the exact OpenClaw device identity before granting write permissions; do not rely on approve-latest behavior.

Risk: Untrusted dates, output paths, or dependency installs can create local file handling or environment risk.

Mitigation: Validate dates and output paths before invoking scripts, keep writes within the skill data directory, and use pinned dependencies in an isolated environment.

## Reference(s):

- [FitBuddy ClawHub skill page](https://clawhub.ai/promisewhh/skills/fitbuddy)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [Initialization guide](references/init-guide.md)
- [Nutrition calculation reference](references/nutrition.md)
- [Nutrition Q&A guide](references/nutrition-guide.md)
- [Exercise guide](references/exercise.md)
- [Training plan guide](references/training-plan.md)
- [Budget meal guide](references/budget-meals.md)
- [Reports and charts guide](references/reports.md)
- [Reminder logic](references/reminder-logic.md)
- [Reminder channel configuration](references/channels.md)
- [McDonald's MCP integration](references/mcd-integration.md)
- [McDonald's MCP endpoint](https://open.mcd.cn/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance, files]

**Output Format:** [User-facing text and Markdown, JSON records and command outputs, shell commands for setup, configuration snippets, and optional PNG chart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local profile, food database, daily record, pattern, and chart files under fitbuddy-data when used as documented.]

## Skill Version(s):

2.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
