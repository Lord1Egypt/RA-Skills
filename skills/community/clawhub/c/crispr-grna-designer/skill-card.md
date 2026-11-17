## Description:

Design CRISPR gRNA sequences for specific gene exons with off-target prediction and efficiency scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and bioinformatics practitioners use this skill to generate candidate CRISPR guide RNAs for targeted gene-editing analysis, including predicted efficiency scores and off-target summaries. Its outputs require independent validation before any real experimental or clinical use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mock guide design and simulated off-target results may be mistaken for production-grade genomic analysis.

Mitigation: Treat outputs as demo data and require independent validation with real sequence retrieval, real off-target analysis, and experimental confirmation before genome-editing decisions.

Risk: The skill runs Python code and can write result files.

Mitigation: Install and run it only in an isolated, low-privilege environment with output paths constrained to the workspace.

Risk: Unpinned Python dependencies may change behavior or increase supply-chain exposure.

Mitigation: Pin and audit dependencies before operational use.

## Reference(s):

- [CRISPR Scoring Algorithms Reference](artifact/references/scoring_algorithms.md)
- [Off-Target Databases](artifact/references/off_target_databases.md)
- [Efficiency Benchmarks](artifact/references/efficiency_benchmarks.md)
- [GUIDE-seq datasets](https://github.com/tsailabSJ/guideseq)
- [Cas-OFFinder](http://www.rgenome.net/cas-offinder/)
- [CHOPCHOP](https://chopchop.cbu.uib.no/)
- [Ensembl REST API](https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene_symbol})

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON results with text guidance and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include candidate guide sequences, PAM sites, predicted efficiency scores, off-target summaries, warnings, and output-file paths.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
