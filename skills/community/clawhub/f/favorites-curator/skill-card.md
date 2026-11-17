## Description:

Build and maintain a local favorites catalog from installed repositories, apps, skills, extensions, and hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luw2007](https://clawhub.ai/user/luw2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to scan local repositories, applications, skills, extensions, and hooks into a file-backed favorites catalog, then generate digest and notification text for notable changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan can collect broad local software inventory, including repositories, applications, skills, extensions, and hooks.

Mitigation: Run it only in an environment where that local inventory collection is acceptable, and review the generated favorites files before sharing them.

Risk: Optional enrichment may contact GitHub or vendor domains using URLs discovered from local inventory.

Mitigation: Run without network access unless disclosing those discovered URLs to external services is acceptable.

Risk: Using --limit-source against an existing catalog can remove entries for sources that were not selected in the limited scan.

Mitigation: Back up favorites/ before limited scans or use a separate workspace until the deletion behavior is fixed.

## Reference(s):

- [Naming And Data Model](references/naming-and-model.md)
- [ClawHub Skill Page](https://clawhub.ai/luw2007/skills/favorites-curator)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text, Shell commands]

**Output Format:** [Markdown catalog entries and reports, JSON snapshots, and short text notifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local favorites catalog under favorites/ and caches optional enrichment results.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
