## Description: <br>
Date/time anti-pattern scanner -- detects timezone bugs, naive datetime usage, hardcoded timestamps, non-ISO formats, incorrect epoch handling, DST-unsafe comparisons, and temporal anti-patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use DateGuard to scan local codebases for date/time anti-patterns, generate quality reports, and optionally enforce checks through git hooks before commits or pushes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads local project files and DateGuard license configuration. <br>
Mitigation: Install only after reviewing the skill behavior, run it on intended project paths, and use trusted license tokens. <br>
Risk: License secrets can be supplied through command-line flags, environment variables, or user configuration. <br>
Mitigation: Prefer the documented environment or configuration path instead of passing license keys directly on the command line. <br>
Risk: Git hook installation can persistently change commit and push behavior through lefthook configuration. <br>
Mitigation: Review the generated lefthook.yml changes and enable hooks only when ongoing DateGuard scans are desired. <br>


## Reference(s): <br>
- [ClawHub DateGuard Release](https://clawhub.ai/suhteevah/dateguard) <br>
- [DateGuard Homepage](https://dateguard.pages.dev) <br>
- [DateGuard Git Hooks Documentation](https://dateguard.pages.dev/docs/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, configuration, guidance] <br>
**Output Format:** [Text reports, JSON, HTML, markdown reports, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free tier scans 30 patterns; paid tiers unlock additional pattern categories and optional git hook integration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
