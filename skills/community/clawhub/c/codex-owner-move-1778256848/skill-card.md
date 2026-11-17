## Description:

Validates owner migration of a ClawHub skill from a personal publisher to an organization publisher with version checks, inspection, and cleanup in a controlled workflow.

This skill is for research and development only.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:

MIT-0

## Use Case:

Maintainers use this skill to validate a temporary ClawHub owner migration flow from a personal publisher to an organization publisher. It supports controlled publish, migration opt-in, version inspection, and cleanup checks for a throwaway skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A maintainer could run the owner migration workflow against a non-throwaway skill and unintentionally publish, migrate, or delete production content.

Mitigation: Verify the skill is a throwaway migration-test skill before publishing, migrating, or deleting anything.

Risk: The workflow is intended for maintainer validation rather than general user installation.

Mitigation: Restrict use to maintainers testing the owner migration flow and avoid installing it as an end-user skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steipete/skills/codex-owner-move-1778256848)
- [Publisher profile](https://clawhub.ai/user/steipete)

## Skill Output:

**Output Type(s):** [guidance]

**Output Format:** [Markdown procedure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintainer-only workflow for validating a throwaway skill owner migration.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
