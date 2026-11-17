## Description:

Visualize gene structure with exon-intron diagrams, domain annotations, and mutation position markers. Produces SVG, PNG, or PDF figures suitable for publication from a gene symbol input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, bioinformatics analysts, and researchers use this skill to generate exon-intron structure figures from gene symbols, optionally adding UniProt domain overlays and mutation position markers for manuscripts, presentations, and exploratory analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted gene identifier can affect the cache path used for local JSON reads or writes.

Mitigation: Run the skill in a sandboxed working directory and validate gene identifiers or hash cache keys before production use.

Risk: The script writes generated figure files to a user-specified output path.

Mitigation: Review output paths before execution and restrict writes to an intended workspace directory.

Risk: Domain overlays are skipped in demo mode and canonical transcript selection excludes alternate isoforms.

Mitigation: Use live gene lookup for domain overlays and verify transcript or isoform assumptions when the figure supports scientific decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/gene-structure-mapper)
- [Ensembl REST API](https://rest.ensembl.org)
- [Ensembl gene symbol lookup endpoint](https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene}?expand=1)
- [EBI Proteins API feature endpoint](https://www.ebi.ac.uk/proteins/api/features/{accession})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands and generated SVG, PNG, or PDF figure files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should state the objective, inputs, assumptions, workflow, output file path, constraints, risks, and next checks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
