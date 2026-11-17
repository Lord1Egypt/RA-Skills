## Description:

Manage Claude Managed Agents end to end through a Python helper CLI, with ant CLI equivalents documented as a secondary path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronfaby](https://clawhub.ai/user/aaronfaby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Claude Managed Agents agents, environments, sessions, event streams, files, configuration, and diagnostics from a local machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad remote-agent lifecycle control can affect agents, environments, sessions, files, and event streams.

Mitigation: Install only when this level of control is needed, verify exact resource IDs before archive or delete actions, and prefer archive before permanent deletion.

Risk: API-key destination and networking choices can send requests or managed-agent traffic to unintended endpoints.

Mitigation: Keep ANTHROPIC_API_BASE_URL unset unless using a trusted HTTPS gateway, and prefer limited networking with explicit allowed hosts.

Risk: File upload and mounted-resource workflows can expose sensitive local files or secrets.

Mitigation: Avoid uploading sensitive files or secrets unless explicitly approved, and review mounted resources before starting or modifying sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaronfaby/skills/claude-managed-agents)
- [Quickstart](references/quickstart.md)
- [Lifecycle Recipes](references/lifecycle-recipes.md)
- [Files API Workflows](references/files-api.md)
- [Event Model and Steering](references/event-model.md)
- [ant CLI Recipes](references/ant-cli-recipes.md)
- [Known Gaps and Assumptions](references/known-gaps.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Concise Markdown with command examples and lifecycle details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON output when the user requests raw API or helper results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
