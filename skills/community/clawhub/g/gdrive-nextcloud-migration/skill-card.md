## Description:

Experimental. Use when migrating Google Drive to Nextcloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5olid5nake](https://clawhub.ai/user/5olid5nake)

### License/Terms of Use:

MIT

## Use Case:

Developers and Nextcloud administrators use this skill to copy a Google Drive tree into Nextcloud, review migration errors, and optionally convert HEIC images and add extensions to files that lack them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration instructions run a script from a predictable shared /tmp path with Nextcloud account privileges, so another local user could replace it.

Mitigation: Before installation, verify the script is staged in a protected location that other local users cannot replace.

## Reference(s):

- [Low-tech Lab migration procedure](https://bureau.lowtechlab.org/apps/collectives/p/YmeZCDHbQnXqGEB/Vers-un-numerique-souverain-et-resilient-9/La-migration-des-donnees-713441)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and bash scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run plans and migration error reports.]

## Skill Version(s):

0.3.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
