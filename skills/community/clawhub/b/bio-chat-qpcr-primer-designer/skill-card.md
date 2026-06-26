## Description: <br>
Advanced RT-qPCR primer and probe design with specialized support for cross-species homology mapping and high-GC virus optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjuphD](https://clawhub.ai/user/zjuphD) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and laboratory users can use this skill to design candidate RT-qPCR primer and TaqMan probe sets for standard transcript assays, predicted transcripts with homolog junction mapping, high-GC viral templates, and optional off-target checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated primer/probe designs may be unsuitable for a specific laboratory assay or biological context. <br>
Mitigation: Independently validate generated primer/probe designs before relying on them in lab work. <br>
Risk: NCBI lookups may disclose accession targets to an external service. <br>
Mitigation: Avoid submitting unpublished or sensitive accession information to NCBI when that disclosure matters. <br>
Risk: The Python dependency is not pinned in the artifact. <br>
Mitigation: Install the skill in a controlled Python environment and pin requests to a vetted current version before use. <br>


## Reference(s): <br>
- [RT-qPCR Primer Design Guidelines](references/guidelines.md) <br>
- [NCBI EFetch endpoint used for sequence and annotation lookups](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi) <br>
- [ClawHub skill release page](https://clawhub.ai/zjuphD/bio-chat-qpcr-primer-designer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-formatted assay candidates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces candidate primer/probe sequences, amplicon size, Tm, length, and gDNA-safety status for user review.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
