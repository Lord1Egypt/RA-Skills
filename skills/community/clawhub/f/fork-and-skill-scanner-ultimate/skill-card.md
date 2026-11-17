## Description:

Reference material, not a runnable skill: a one-page outline of a workflow for scanning GitHub forks and ClawHub skills (bash pre-filter, sub-agent fan-out, scheduled reports). It ships no scripts and has no entry point. Read it only for the workflow shape; for working scanner code use the sibling skills/fork-scanner/ directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this as reference material for designing a fork-and-skill scanning workflow. It outlines pre-filtering, sub-agent fan-out, scoring, and report assembly, but it does not run scans itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the package for a working scanner.

Mitigation: Confirm there is no entry point before use; treat the artifact as workflow reference material only.

Risk: A separate implementation of the described workflow may introduce token handling, network access, scheduled jobs, and output path risks.

Mitigation: Review that separate implementation for credential handling, network behavior, cron configuration, and output locations before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/fork-and-skill-scanner-ultimate)
- [TinkerClaw repository referenced by artifact](https://github.com/globalcaos/tinkerclaw)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown reference material]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only package; it produces no files, shell commands, API calls, or automated scanner output.]

## Skill Version(s):

1.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
