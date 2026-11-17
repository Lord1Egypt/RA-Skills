## Description:

Finml Toolkit logs, searches, summarizes, and exports timestamped records for financial machine learning workflow activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to record financial ML operations, inspect recent activity, search previous entries, and export local audit logs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-entered financial workflow details may be retained in plaintext local logs and export files.

Mitigation: Avoid entering credentials, account identifiers, private strategy details, or regulated data, and review stored logs and exports before sharing or retaining them.

Risk: The package description and implementation are inconsistent, including documented data-directory behavior that may not be honored by the script.

Mitigation: Confirm the installed script behavior before relying on it, especially the data directory, retention expectations, and deletion process.

Risk: Local audit logs may persist without explicit retention or deletion controls.

Mitigation: Apply local file retention practices, restrict access to the data directory, and delete logs and exports when they are no longer needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text command output with local log and export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes command logs, history logs, and json, csv, or txt exports under the local finml-toolkit data directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
