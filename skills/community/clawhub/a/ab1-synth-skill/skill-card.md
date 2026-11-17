## Description:

Generate a synthetic Sanger .ab1 chromatogram from a reference FASTA (ASV/consensus) plus raw FASTQ reads, with realistic peak spacing/height/width, baseline noise and minor peaks, and a Chromas-compatible ABIF container.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zd200572](https://clawhub.ai/user/zd200572)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bioinformatics researchers can turn a reference FASTA and optional supporting reads into a synthetic chromatogram for viewing in common sequence-analysis tools. The trace is simulated and should not be presented as instrument data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-controlled output path may enable command execution when automatic opening is used, particularly on Windows or supported WSL.

Mitigation: Avoid automatic opening for untrusted output paths. Use a trusted output location and review the generated file before opening it; the security scan is partial.

## Reference(s):

- [ClawHub release](https://clawhub.ai/zd200572/skills/ab1-synth-skill)
- [Source repository](https://github.com/zd200572/ab1-synth-skill)
- [Publisher profile](https://clawhub.ai/user/zd200572)

## Skill Output:

**Output Type(s):** [Files]

**Output Format:** [Synthetic ABIF chromatogram file (.ab1)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Simulated trace, not instrument data; optional read-derived peak variation and quality effects.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
