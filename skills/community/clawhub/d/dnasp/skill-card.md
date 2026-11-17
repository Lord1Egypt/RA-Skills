## Description:

Analyzes pre-aligned DNA sequences or multi-sample VCFs using selected DnaSP 6 population-genetics methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drdaviddelorenzo](https://clawhub.ai/user/drdaviddelorenzo)

### License/Terms of Use:

MIT

## Use Case:

Researchers and developers use this skill to calculate diversity, neutrality, linkage disequilibrium, divergence and coding-sequence statistics from aligned DNA or multi-sample VCF data. It does not align or phase sequences or provide clinical interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reproducibility bundle stores copies of supplied DNA/VCF and metadata files, which may contain sensitive genetic information.

Mitigation: Use a private output location; restrict or delete the bundle before sharing results.

## Reference(s):

- [Server-resolved skill source](https://github.com/drdaviddelorenzo/dnasp/tree/main/skills/dnasp)
- [Project repository](https://github.com/drdaviddelorenzo/dnasp)
- [DnaSP 6 methods paper](https://doi.org/10.1093/molbev/msx248)
- [Statistical reference](docs/index.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, TSV, PNG figures]

**Output Format:** [Local Markdown report, JSON summaries, TSV tables and optional PNG figures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a reproducibility bundle with archived inputs and commands; figures and pairwise LD tables are conditional.]

## Skill Version(s):

0.6.1 (source: SKILL.md frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
