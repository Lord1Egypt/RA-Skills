## Description:

Provides guidance and helper scripts for BLAST-based species annotation from FASTA sequences or top ASVs extracted from OTU tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zd200572](https://clawhub.ai/user/zd200572)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, bioinformatics analysts, and researchers use this skill to prepare and run NCBI BLAST species annotation workflows for sequence FASTA files and OTU-table top ASVs. It helps generate per-sample BLAST result CSVs, a BLAST summary table, and top-ASV information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OTU table sample names can cause CSV output to be written outside the intended output folder.

Mitigation: Run only on trusted OTU tables or sanitize sample names before use; execute in an isolated project directory or virtual environment without administrator privileges.

Risk: BLAST requests send sequence data to NCBI.

Mitigation: Do not process proprietary or sensitive sequence data unless sharing it with NCBI is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zd200572/skills/blast-species-identification)
- [Publisher profile](https://clawhub.ai/user/zd200572)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and parameter descriptions; the included scripts produce CSV result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Biopython and network access to NCBI BLAST; supports request delay, hit count, mapping files, OTU tables, and skip-existing behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
