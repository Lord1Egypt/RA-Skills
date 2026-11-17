## Description:

Documents a maintainer-only ClawHub owner migration validation workflow.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:

MIT-0

## Use Case:

ClawHub maintainers use this skill to validate moving a temporary skill from a personal publisher to an organization owner, checking version history and cleanup behavior after the move.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Owner migration validation can alter or delete a skill record if run against a non-temporary release.

Mitigation: Run it only against a throwaway skill record with the intended permissions, then delete the temporary skill after validation.

Risk: The workflow is not a general-purpose user skill and may be misapplied outside maintainer testing.

Mitigation: Install or use it only for maintainer validation of ClawHub owner migration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steipete/skills/codex-owner-move-1778256696)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown prose with numbered validation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintainer-only checklist; no executable code in the artifact.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
