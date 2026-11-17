## Description:

Ghostclaw Clone helps agents review code architecture, identify system-level flow issues, suggest refactors, monitor repository health, and optionally prepare architectural improvement PRs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ev3lynx727](https://clawhub.ai/user/ev3lynx727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use Ghostclaw Clone to analyze codebases for architectural health, coupling, cohesion, naming, layering, and stack alignment. It can produce one-shot reports, delta-focused PR review guidance, background monitoring summaries, and optional PR preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal analysis can automatically run Python plugins from the repository being analyzed.

Mitigation: Run the skill in an isolated environment and analyze only trusted repositories, or remove or disable any .ghostclaw/plugins directory before analysis.

Risk: The npm package includes a postinstall PATH change.

Mitigation: Review the npm postinstall behavior before installation, or install and test in an isolated environment first.

Risk: Optional watcher, systemd service, and --create-pr behavior can create persistent automation or GitHub PR activity.

Mitigation: Enable these modes only after reviewing their configuration and token access; avoid --create-pr unless PR automation is intended.

Risk: Default review runs can save local architecture reports.

Mitigation: Use --no-write-report when local report files should not be created.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ev3lynx727/skills/ghostclaw-clone)
- [Ghostclaw Guide](docs/GUIDE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Delta-Context Analysis Examples](docs/examples/delta-analysis.md)
- [Stack Patterns](src/ghostclaw/references/stack-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON analysis data, inline code suggestions, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write timestamped architecture reports locally unless --no-write-report is used; optional PR creation requires gh CLI and token configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
