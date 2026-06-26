## Description: <br>
Provides guidance and helper scripts for BLAST-based species annotation from FASTA sequences or top ASVs extracted from OTU tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zd200572](https://clawhub.ai/user/zd200572) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics users can use this skill to prepare and run NCBI BLAST annotations for sequence FASTA files or representative ASVs from OTU tables, then review CSV result and summary files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted OTU table can cause one script to write result files outside the chosen output folder. <br>
Mitigation: Use a dedicated output directory and sanitize or inspect sample column names for path traversal, absolute paths, and other filename tricks before running the script. <br>
Risk: Sequence data is submitted to NCBI BLAST during normal operation. <br>
Mitigation: Avoid running private sequence data unless submission to NCBI is acceptable for the dataset. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zd200572/blast-species-identification) <br>
- [Artifact usage guide](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and Python scripts that write CSV result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Biopython and network access to NCBI BLAST; script outputs include per-sample BLAST CSV files, blast_summary.csv, and top_asv_info.csv.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
