## Description:

Manage a Bring! shopping list by adding, removing, completing, and checking items through a Bring! account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zahlmann](https://clawhub.ai/user/zahlmann)

### License/Terms of Use:

MIT

## Use Case:

External users with a Bring! account use this skill to let an agent add, remove, complete, and list groceries from the account's default shopping list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Bring! account credentials and can expose shopping-list contents to the agent.

Mitigation: Store credentials outside project files, avoid reusing the Bring! password, and use the skill only in trusted workspaces.

Risk: The skill uses a live external Bring! API through an unofficial Python package.

Mitigation: Review requested list changes before execution and expect behavior to depend on Bring! and bring-api availability.

Risk: Python dependencies are unpinned in requirements and uv examples.

Mitigation: Pin or lock bring-api and python-dotenv before regular use.

## Reference(s):

- [Bring!](https://www.getbring.com/)
- [bring-api Python package](https://github.com/miaucl/bring-api)
- [uv documentation](https://docs.astral.sh/uv/)
- [Agent Skills specification](https://agentskills.io/specification)
- [ClawHub skill page](https://clawhub.ai/zahlmann/skills/bring-shopping-list)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus CLI JSON or text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the first default Bring! shopping list and supports optional item specifications with name:spec syntax.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
