## Description:

BenchClaw evaluates OpenClaw agents across capability, configuration, security, hardware, and permission tasks, then produces scores and reports for performance, cost, and safety comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antutuadmin](https://clawhub.ai/user/antutuadmin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use BenchClaw to run a 25-task OpenClaw benchmark, compare score dimensions, and generate local or optionally uploaded leaderboard reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote benchmark questions drive the user's main OpenClaw agent during evaluation.

Mitigation: Run the skill only in an isolated disposable OpenClaw profile or workspace with no sensitive files or credentials.

Risk: Leaderboard upload is enabled unless the caller disables it, and submitted per-question output can include truncated stdout or stderr.

Mitigation: Set temp/caller_info.txt to upload_to_server=false unless leaderboard submission is explicitly intended.

Risk: Stdout and stderr sanitization is best effort and may not remove every sensitive value.

Mitigation: Avoid running benchmarks in environments containing secrets, and review generated reports before sharing them.

Risk: Failed uploads can be cached for later submission when upload remains enabled.

Mitigation: Clear cached submissions after failed uploads if the user does not want results submitted later.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/antutuadmin/skills/benchclaw)
- [BenchClaw homepage](https://benchclaw.antutu.com)
- [BenchClaw leaderboard](https://benchclaw.antutu.com/leaderboard)
- [Repository listed in skill metadata](https://github.com/BenchClaw/benchclaw)
- [Upload disclosure](UPLOAD_DISCLOSURE.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown score reports, JSON result data, and concise progress or result text with setup and execution commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local report files and may submit leaderboard data when upload is enabled.]

## Skill Version(s):

1.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
