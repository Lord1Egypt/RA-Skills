## Description: <br>
Installs 425 bioinformatics skills covering sequence analysis, RNA-seq, single-cell, variant calling, metagenomics, structural biology, and 56 more categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djemec](https://clawhub.ai/user/djemec) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and bioinformatics practitioners use BioSkills to add specialized OpenClaw skills for genomics, transcriptomics, single-cell analysis, variant analysis, metagenomics, structural biology, and related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing all BioSkills changes the agent's future skill-trigger surface. <br>
Mitigation: Use a dry run or category-limited install first, and update or uninstall bio-* skills when the expanded surface is no longer wanted. <br>
Risk: The installer clones an external BioSkills release and writes skills into the local OpenClaw skills directory. <br>
Mitigation: Review the bundled installer before execution and rely on its pinned release tag and expected commit verification during installation. <br>


## Reference(s): <br>
- [BioSkills ClawHub Release](https://clawhub.ai/djemec/bioskills) <br>
- [BioSkills source repository listed in artifact](https://github.com/GPTomics/bioSkills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and installation options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs all BioSkills by default, with category-limited, update, and uninstall modes available through the bundled shell script.] <br>

## Skill Version(s): <br>
3.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
