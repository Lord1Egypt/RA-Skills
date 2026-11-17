## Description:

datefmt-lite helps agents convert and format dates and times, including ISO 8601, Unix epoch, RFC 2822, timezone conversion, duration arithmetic, and cron weekday checks, using only GNU date and the local TZ database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need local shell recipes for timestamp conversion, timezone rendering, duration math, cron sanity checks, or quick log-friendly date formatting without external APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipes and duration helper depend on GNU date and a local TZ database, so behavior may fail or differ on systems that only provide BSD date.

Mitigation: Confirm GNU coreutils date is available before use; on macOS, install coreutils and use gdate or the documented g-prefix convention.

Risk: Persisting local-zone date strings can create ambiguous or incorrectly sorted logs across daylight saving time boundaries.

Mitigation: Use UTC, Unix epoch seconds, or date strings that include an explicit timezone when recording durable timestamps.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline bash code blocks and short shell-script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local GNU date commands and a duration helper script; no network calls, credentials, persistence, or destructive behavior were reported by security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
