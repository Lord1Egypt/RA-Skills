## Description:

Designs RT-qPCR primers and TaqMan probes with support for cross-species homology mapping, high-GC templates, exon-junction checks, and 3' specificity review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjuphd](https://clawhub.ai/user/zjuphd)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and laboratory developers use this skill to generate candidate SYBR or TaqMan RT-qPCR assay designs from NCBI accessions or local FASTA sequences. It is aimed at standard transcript targets, predicted transcripts that may need homolog-based junction mapping, and high-GC viral templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accession-based lookups contact NCBI, so queried accession identifiers may leave the local environment.

Mitigation: Use local FASTA input or run accession lookups only where external NCBI requests are acceptable.

Risk: The Python dependency list includes requests without a version pin.

Mitigation: Pin requests or use a reviewed lock file before installing in sensitive or reproducibility-critical environments.

Risk: When exon junctions cannot be found or mapped, candidate designs can report gDNA safety as Unknown.

Mitigation: Treat Unknown gDNA safety outputs as candidates requiring domain review before laboratory use.

## Reference(s):

- [RT-qPCR Primer Design Guidelines](artifact/references/guidelines.md)
- [ClawHub skill page](https://clawhub.ai/zjuphd/skills/bio-chat-qpcr-primer-designer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON assay result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces candidate primer/probe sets with amplicon size, Tm, length, and gDNA safety status.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
