## Description:

Argus scans Python or JavaScript codebases for bugs, security vulnerabilities, code smells, and common anti-patterns, producing prioritized findings with line numbers, severity ratings, and fix suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Argus to scan Python or JavaScript projects locally and receive prioritized bug, security, and code-quality findings before review or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install step modifies the Python environment.

Mitigation: Install and run the skill in an isolated virtual environment.

Risk: Generated reports may contain local file paths and code excerpts.

Mitigation: Review report files before sharing them and avoid scanning broad or sensitive directories unless those details are acceptable.

## Reference(s):

- [Argus ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/argus1)
- [Argus ClawHub homepage](https://clawhub.ai/occupythemilkyway/argus1)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Console report plus local Markdown report; optional JSON report when OUTPUT_JSON is true.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include file paths, line numbers, severity ratings, code excerpts, and fix suggestions.]

## Skill Version(s):

1.0.4 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
