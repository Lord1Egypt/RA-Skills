## Description: <br>
Visualize gene structure with exon-intron diagrams, domain annotations, and mutation position markers. Produces SVG, PNG, or PDF figures suitable for publication from a gene symbol input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate gene structure figures from gene symbols or Ensembl IDs for manuscripts, presentations, and exploratory bioinformatics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live lookups send gene symbols and species names to public bioinformatics APIs. <br>
Mitigation: Use demo mode for offline TP53 examples, or avoid live lookup when gene or species names should not be shared with public APIs. <br>
Risk: User-selected output paths can overwrite existing files. <br>
Mitigation: Choose a dedicated output path and check for existing files before running figure generation. <br>
Risk: Cached Ensembl responses may be stale when fresh annotations are required. <br>
Mitigation: Clear the relevant .cache entry before regenerating figures that require current annotations. <br>
Risk: The skill visualizes only the canonical transcript and domain mapping can be less accurate for complex splicing. <br>
Mitigation: Review transcript choice and annotation assumptions before using figures in publication or downstream analysis. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AIPOCH-AI/gene-structure-mapper) <br>
- [Publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>
- [Ensembl REST API](https://rest.ensembl.org) <br>
- [Ensembl gene lookup endpoint](https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene}?expand=1) <br>
- [EBI Proteins API](https://www.ebi.ac.uk/proteins/api/features/{accession}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated SVG, PNG, or PDF figure files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated figures may use live Ensembl and UniProt data or the offline TP53 demo dataset.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
