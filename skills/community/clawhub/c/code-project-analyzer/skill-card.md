## Description:

Analyzes a local code directory to identify its technology stack, module structure, core functions, use cases, and implementation principles, then generates a standardized Markdown project introduction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttjsndx](https://clawhub.ai/user/ttjsndx)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to quickly understand unfamiliar local repositories and generate README-style project summaries covering functionality, architecture, technology stack, and reuse scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local project folders and may include sensitive repository details in generated summaries.

Mitigation: Run it only on projects intended for analysis and avoid repositories containing secrets or private business code unless that disclosure is intended.

Risk: Generated summaries can be incomplete or misleading because they are inferred from file names, package metadata, README excerpts, and shallow directory scans.

Mitigation: Review the Markdown output before sharing it or using it as authoritative documentation.

Risk: The skill can create a Markdown summary file in the target or requested output path.

Mitigation: Choose the output path deliberately and inspect the file diff before committing generated documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ttjsndx/skills/code-project-analyzer)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown project summary, primarily in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a project introduction Markdown file to the requested output path.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
