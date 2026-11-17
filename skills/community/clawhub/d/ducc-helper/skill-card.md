## Description:

ducc-helper lets agents inspect, edit, delete, and release JD DUCC configuration through command-line workflows with local JD ME SSO authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oilvegetable](https://clawhub.ai/user/oilvegetable)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to read JD DUCC namespaces, config files, profiles, and key-value items, and to manage draft changes and releases. It is intended for authorized DUCC operators who need terminal-based configuration workflows, including dry-run release planning and staged rollout support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect production JD DUCC configuration when release commands are confirmed.

Mitigation: Use it only from authorized machines and require human review before draft deletion or any release with --confirm, especially against the online environment.

Risk: The skill handles reusable company login cookies and caches authentication material locally.

Mitigation: Protect the local cache, clear ~/.ducc-helper-cache.json when finished, and avoid running the authentication module directly unless needed.

Risk: DUCC API traffic uses HTTP endpoints according to the artifact and evidence guidance.

Mitigation: Confirm that this transport is acceptable on the relevant corporate network before installing or operating the skill.

Risk: Incorrect configuration edits may be staged in drafts before release.

Mitigation: Review generated plans and JSON output before release, prefer gray release paths for production changes, and keep the default dry-run behavior until ready to execute.

## Reference(s):

- [DUCC API reference](artifact/references/api.md)
- [ClawHub skill page](https://clawhub.ai/oilvegetable/skills/ducc-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command scripts print JSON on stdout and progress or warnings on stderr.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
