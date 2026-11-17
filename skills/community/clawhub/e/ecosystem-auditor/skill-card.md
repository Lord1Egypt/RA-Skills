## Description:

Audits a local WorkBuddy skill ecosystem for frontmatter validity, Python script syntax, stale skills, near duplicates, and orphaned meta-skills, then reports structured findings for maintenance decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit a local skill directory before release or during maintenance, identifying malformed skill metadata, Python syntax errors, stale entries, near duplicates, and orphaned meta-skills. Meta-evolution workflows can use the structured report to decide what to repair, merge, or retire.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The auditor reads local skill directories, which may contain private notes, unpublished skill logic, or sensitive examples.

Mitigation: Run it only against intended skill roots and avoid storing secrets or sensitive user content in skill files that will be audited.

Risk: The learner helper can write learned_patterns.json files containing usage notes and preferences.

Mitigation: Call learner.py only with intended skill directories and do not put secrets or sensitive user content into learner notes.

Risk: Staleness and near-duplicate findings are heuristic and can produce false positives or miss issues.

Mitigation: Tune stale_days and dup_threshold for the size of the ecosystem, then review findings before repair, merge, or removal decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/ecosystem-auditor)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell commands and JSON health reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include summary counts and lists for broken, stale, duplicate, and orphaned skills.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
