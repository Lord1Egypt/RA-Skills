## Description:

Build or improve a top-tier AI conference paper workflow for NeurIPS, ICML, ICLR, and similar venues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hayashishungenn](https://clawhub.ai/user/hayashishungenn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to scaffold and manage AI conference paper projects, including literature review, experiment planning, drafting, review, revision, and reusable project file setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive broad file creation and persistent Git commits in a research-paper repository.

Mitigation: Require explicit approval before file creation, package installs, external API calls, and each Git commit.

Risk: Credential-adjacent logs or progress files could expose API keys or token values.

Mitigation: Record only environment variable names and configuration status; never write secret values into PROGRESS.md, logs, or commits.

Risk: Automated paper workflows can introduce fabricated experiments, fake citations, or unsupported claims.

Mitigation: Require evidence review for experiments, datasets, ablations, statistical tests, citations, and methodology-to-result consistency before using generated paper content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hayashishungenn/skills/ai-paper-pipeline)
- [Full pipeline template](artifact/references/full-pipeline-template.md)
- [Project scaffold](artifact/references/project-scaffold.md)
- [Project mega prompt template](artifact/templates/MEGA_PROMPT.project.md)
- [Progress template](artifact/templates/PROGRESS.template.md)
- [Restrictions example](artifact/templates/RESTRICTS.example.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance plus workspace files such as project templates, YAML configuration, LaTeX scaffolds, plans, code directories, and progress logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify workspace files and Git commits when appropriate.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
