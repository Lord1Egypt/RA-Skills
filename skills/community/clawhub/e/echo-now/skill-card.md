## Description:

Print the current UTC time and ISO date in a deterministic, copy-friendly format. Use when an agent or operator needs a stable timestamp string for logs, file names, notes, or manifests and wants a single reusable command instead of rewriting date formatting each time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to produce stable UTC timestamp and date strings for logs, file names, notes, and manifests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timestamp accuracy depends on the host system clock and the POSIX date command being available.

Mitigation: Run the skill in an environment with a synchronized clock and POSIX date available on PATH.

Risk: Some environments may restrict direct script execution permissions.

Mitigation: Use normal approved shell execution controls, or run the script through sh when executable permissions are not set.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text with two key-value lines: utc=<YYYY-MM-DDTHH:MM:SSZ> and date=<YYYY-MM-DD>]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the local POSIX date command and UTC formatting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
