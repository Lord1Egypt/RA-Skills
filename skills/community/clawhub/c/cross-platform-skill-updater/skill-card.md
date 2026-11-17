## Description:

Checks and updates locally installed skills from git worktrees or .skill-lock.json lockfiles across common AI coding tool directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viccwang](https://clawhub.ai/user/viccwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local skill installations, identify available updates, and apply safe updates across supported agent tooling directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Update mode can replace local agent skill files from lockfile paths and sources that may not be sufficiently validated.

Mitigation: Run check first on an explicit --path, inspect each reported source and path, and avoid update on lockfiles you did not create or trust.

Risk: Default scanning can inspect common project and user-level skill directories.

Mitigation: Use --path to limit scope when reviewing or updating a specific provider root.

Risk: The security verdict is suspicious due to review-worthy replacement behavior.

Mitigation: Review and scan the skill before deployment, and add path-containment and source-validation safeguards before trusting broad update workflows.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/viccwang/skills/cross-platform-skill-updater)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and optional structured JSON status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scan project and user-level skill directories; update mode can replace local skill files when checks pass.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
