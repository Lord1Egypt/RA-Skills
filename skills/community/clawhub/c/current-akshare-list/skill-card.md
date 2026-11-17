## Description:

Fetches Chinese A-share, B-share, Beijing Stock Exchange, and STAR Market stock lists with AkShare, cross-checks real-time quote lists, and saves current trading and non-trading stock CSV files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-data analysts use this skill to refresh Chinese stock universe lists, compare them against real-time AkShare quote endpoints, and produce CSV outputs for trading and non-trading securities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suggests recurring cron-based retry tasks when the Eastmoney-backed AkShare endpoint is blocked, which could continue running without enough user oversight.

Mitigation: Require explicit user approval for the exact command, schedule, timeout, output path, and self-removal behavior; prefer manual retry or bounded in-process retry when possible.

Risk: The skill runs Python code that installs or imports AkShare and makes outbound market-data requests.

Mitigation: Review the script before installation or execution and run it only in an environment where outbound market-data access is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ugpoor/skills/current-akshare-list)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell snippets plus generated CSV and temporary JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected files include stocklist.csv, stocklist_intrading.csv, notspot.csv, and temporary AkShare quote JSON files under /tmp.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
