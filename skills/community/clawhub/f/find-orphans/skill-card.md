## Description:

Finds orphaned files, unused components, and dead code in projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect front-end TypeScript and JavaScript projects for orphaned files, unused components, uncalled utilities, and route, style, or asset references that may be safe to remove.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Static cleanup analysis can misclassify files that are referenced through dynamic imports, convention-based routes, feature flags, tests, service workers, or public assets.

Mitigation: Treat findings as heuristic, review every proposed orphan manually, and run the project build and tests before committing removals.

Risk: A generated deletion script can remove project files if executed without review.

Mitigation: Generate deletion scripts only after explicit user confirmation, inspect each command, and perform cleanup on a version-controlled branch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzhiming1999/skills/find-orphans)
- [Artifact repository URL](https://github.com/wangzhiming1999/oliver-skill)
- [Artifact homepage URL](https://github.com/wangzhiming1999/oliver-skill/tree/main/skills/find-orphans)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown cleanup report with an optional bash deletion script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deletion scripts are generated only after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
