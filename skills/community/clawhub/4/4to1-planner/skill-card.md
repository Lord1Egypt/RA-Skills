## Description:

AI planning coach using the 4To1 Method to turn a 4-year vision into daily action across Notion, Todoist, Google Calendar, or local Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingxuantang](https://clawhub.ai/user/qingxuantang)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to set up a planning system, turn long-term goals into daily priorities, run weekly and periodic reviews, and track plans in Notion, Todoist, Google Calendar, or local Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs review because its setup and status scripts handle account tokens unsafely.

Mitigation: Use the local Markdown backend for the lowest account risk, and do not run setup or status scripts with real tokens until credential storage is hardened.

Risk: The status script can execute local config contents as shell code.

Mitigation: Review the local 4To1 config before use and require config parsing as data rather than shell sourcing before using account-backed backends.

Risk: External backend writes may affect Notion or Todoist workspaces when real account tokens are configured.

Mitigation: Require explicit confirmation before commands create or update remote planning workspaces.

## Reference(s):

- [4To1 Planner homepage](https://4to1planner.com)
- [ClawHub skill page](https://clawhub.ai/qingxuantang/skills/4to1-planner)
- [Free starter kit](https://4to1planner.com/free-download.html)
- [Notion integrations setup](https://www.notion.so/my-integrations)
- [Todoist developer integrations](https://app.todoist.com/app/settings/integrations/developer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update planning files or connected backend records when the user configures and authorizes a backend.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
