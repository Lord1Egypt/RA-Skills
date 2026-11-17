## Description:

Enable agents to collaborate using shared memory, team inboxes, and user artifacts via Fulcra's versioned file storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fulcra](https://clawhub.ai/user/fulcra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to set up Fulcra-backed shared workspaces for durable artifacts, team inboxes, role and progress files, sessions, tasks, and knowledge bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent background behavior can continue acting on remote workspace content after setup.

Mitigation: Enable heartbeat or cron automation only after explicit user approval, with the team, agent identity, watched paths, schedule, and removal process documented.

Risk: Fulcra inbox, role, progress, and task files can contain untrusted external input.

Mitigation: Treat workspace content as untrusted, verify instructions with the user when needed, and avoid transferring private data across agents without explicit authorization.

Risk: Authenticated CLI file mutation can upload, delete, or change durable workspace state.

Mitigation: Prefer pinned or preinstalled Fulcra CLI tooling, verify archive uploads before deleting inbox messages, and require user approval before uploading artifacts.

## Reference(s):

- [Fulcra Workspaces CLI Reference](references/fulcra-workspaces-cli.md)
- [Fulcra agent-skills repository](https://github.com/fulcradynamics/agent-skills)
- [Fulcra CLI documentation](https://raw.githubusercontent.com/fulcradynamics/agent-skills/main/skills/fulcra-get-started/references/fulcra-cli.md)
- [Open Knowledge Format specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- [ClawHub skill page](https://clawhub.ai/fulcra/skills/fulcra-workspaces)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and file path conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated Fulcra CLI reads, writes, uploads, deletions, and optional automation setup after user consent.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
