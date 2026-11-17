## Description:

Elegant Sync backs up and synchronizes selected OpenClaw workspace memory, configuration, and custom skill files with versioned Git branches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russellfei](https://clawhub.ai/user/russellfei)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to preview, back up, and synchronize selected local workspace assets such as memory, agent configuration files, and custom skills to a private repository for recovery across machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive OpenClaw data or repository tokens may be exposed during backup and sync.

Mitigation: Use only a private, access-controlled repository and a narrowly scoped token, and review what will be synchronized before running a real sync.

Risk: Unsafe command construction or token handling may allow unintended command execution or credential disclosure.

Mitigation: Do not run sync until command construction and token handling have been reviewed and fixed.

Risk: Recursive filtering and restore behavior may not fully protect secrets or provide a reliable recovery path.

Mitigation: Fix recursive secret filtering, add confirmation prompts, and validate restore documentation before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/russellfei/skills/elegant-sync)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Console text, Git operations, and local backup files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports sync, dry-run preview, targeted memory or skills sync, restore placeholder, and status output.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
