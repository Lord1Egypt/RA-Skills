## Description: <br>
Designs and ranks preliminary CRISPR/Cas9 sgRNA candidates for viral and microbial genomes, with high-GC scoring logic and donor-template mutation suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjuphD](https://clawhub.ai/user/zjuphD) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics researchers use this skill to generate preliminary sgRNA candidate lists for viral or microbial genome editing workflows, especially high-GC templates. Outputs should be verified with dedicated off-target analysis, donor-design tooling, and appropriate biosafety review before laboratory use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated sgRNA candidates may be mistaken for validated CRISPR designs. <br>
Mitigation: Treat outputs as preliminary candidate generation and verify them with dedicated off-target analysis, donor-design tools, and appropriate biosafety or institutional review. <br>
Risk: Accession-based sequence lookup sends requests to NCBI E-utilities. <br>
Mitigation: Use direct sequence input when external NCBI queries are not acceptable for the workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zjuphD/crispr-sgrna-designer) <br>
- [NCBI E-utilities EFetch endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession}&rettype=fasta&retmode=text) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and JSON candidate records from the bundled Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Candidate sgRNA records include sequence, PAM, score, strand or cut-position details when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
