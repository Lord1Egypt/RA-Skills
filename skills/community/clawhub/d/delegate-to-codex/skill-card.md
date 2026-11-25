## Description:

Guides Claude Code users through explicitly requested Codex delegation, from model selection and handoff through diff review and commit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[troioi-vn](https://clawhub.ai/user/troioi-vn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when they explicitly choose to hand repository work from Claude Code to Codex CLI. It guides them in creating a bounded handoff, reviewing returned changes, and managing Git history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handoff prompts and repository content may be sent to the configured model provider, and each run uses the user's quota or billing.

Mitigation: Delegate only content the user is comfortable sharing with that provider, and choose the model and effort deliberately.

Risk: A long-running delegated task may continue after the interactive session ends.

Mitigation: Check the run's completion and review its returned changes before relying on them.

Risk: Security analysis was partial because some local references could not be resolved.

Mitigation: Review the installed skill and verify its referenced material before use.

## Reference(s):

- [Codex CLI documentation](https://developers.openai.com/codex/cli)
- [ClawHub release page](https://clawhub.ai/troioi-vn/skills/delegate-to-codex)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Files]

**Output Format:** [Markdown handoff prompts, shell commands, and delegated repository changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated code and files depend on the task and are returned for review.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
