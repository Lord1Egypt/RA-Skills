## Description:

Provides best-practice bioinformatics engineering guidance for conda environment management, secrets isolation, Git and DVC data versioning, relative paths, and reusable pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biociao](https://clawhub.ai/user/biociao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bioinformatics engineers use this skill to plan, scaffold, document, and audit reproducible bioinformatics workflows. It guides agents toward established ecosystem tools, project-root-relative paths, Git and DVC versioning, quality checks, and reusable Snakemake, WDL, or DVC pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes templates that load `.env` files with `source .env`, which can execute shell content if the file is not trusted.

Mitigation: Use a non-executing dotenv parser for secrets and review any generated shell template before running it.

Risk: The skill describes automatic inspection of shell profile files to find conda or mamba configuration.

Mitigation: Inspect shell profiles only after explicit user consent and limit reads to the configuration needed for the active task.

Risk: Generated logs may contain sensitive paths, sample identifiers, or credentials if redaction is incomplete.

Mitigation: Treat logs as sensitive until reviewed, apply secret filtering, and avoid logging credentials or identifiable sample data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biociao/skills/bioinfo-engineer-skill)
- [Bioconda](https://bioconda.github.io/)
- [DVC documentation](https://dvc.org/doc)
- [Snakemake documentation](https://snakemake.readthedocs.io/)
- [Nextflow documentation](https://www.nextflow.io/docs/latest/index.html)
- [BioContainers](https://quay.io/organization/biocontainers)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, YAML, Python, R, and workflow snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes project templates, checklists, command examples, and reproducibility guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
