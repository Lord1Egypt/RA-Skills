## Description:

Validates end-to-end skill owner migration by publishing, transferring with a migration flag, verifying, and cleaning up a temporary ClawHub skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:

MIT-0

## Use Case:

Maintainers use this skill to validate ClawHub owner migration for a throwaway skill slug, including publish, transfer, inspection, and cleanup steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for maintainer-only owner-migration validation and should not be installed for normal user workflows.

Mitigation: Use it only in a maintainer test context with the intended throwaway slug and confirmed ClawHub publisher permissions.

Risk: The workflow includes publish, owner-migration, and cleanup actions in ClawHub.

Mitigation: Run the procedure only against temporary validation releases and confirm cleanup after inspection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steipete/skills/codex-owner-move-1778256762)
- [ClawHub publisher profile](https://clawhub.ai/user/steipete)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintainer-only validation flow for a throwaway skill slug.]

## Skill Version(s):

0.0.1 (source: server release evidence, created 2026-05-08T16:12:45Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
