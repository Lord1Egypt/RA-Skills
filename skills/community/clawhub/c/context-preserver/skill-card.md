## Description:

Context Preserver helps agents create, restore, manage, import, and export local context snapshots, including automatic snapshots and session handoff records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to save local session context before task boundaries, recover prior context snapshots, and export or import snapshots for handoff or backup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe path handling may let snapshot commands access JSON files outside the intended snapshot folder.

Mitigation: Use only trusted snapshot IDs and import files, and avoid delete, import, and export commands on untrusted input until snapshot ID validation and path containment are fixed.

Risk: Exported snapshots may reveal local paths and environment details.

Mitigation: Inspect exported snapshot files before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/context-preserver)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON files, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON snapshot data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and manages local files under ~/.context-preserver.]

## Skill Version(s):

1.1.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
