## Description:

Guides agents in installing, switching, restoring, validating, and publishing ClawSouls personas for supported agent workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomleelive](https://clawhub.ai/user/tomleelive)

### License/Terms of Use:

Apache 2.0

## Use Case:

Agent users and developers use this skill to manage workspace personas, browse and publish Souls, and optionally sync encrypted agent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Switching or restoring a persona changes active agent identity files.

Mitigation: Confirm before changing personas and retain workspace backups for restoration.

Risk: Publishing a Soul can expose sensitive files through the public registry.

Mitigation: Confirm publication and review the Soul directory for secrets before uploading it.

Risk: Optional memory sync sends encrypted agent memory to a configured Git remote.

Mitigation: Run sync only on explicit request and confirm the remote and data being synced.

Risk: Unpinned package execution paths can run a different CLI version than the one documented for this release.

Mitigation: Prefer the pinned CLI version or a reviewed local installation over unpinned wrappers and adapter commands.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tomleelive/skills/clawsouls-skill)
- [ClawSouls registry](https://clawsouls.ai)
- [Soul-Driven Interaction Design](https://doi.org/10.5281/zenodo.18772585)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persona files or exported prompts may be produced when the suggested commands are run.]

## Skill Version(s):

0.6.6 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
