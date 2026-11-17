## Description:

Installs 425 bioinformatics skills covering sequence analysis, RNA-seq, single-cell, variant calling, metagenomics, structural biology, and 56 more categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djemec](https://clawhub.ai/user/djemec)

### License/Terms of Use:


## Use Case:

External users, developers, and bioinformatics practitioners use this meta-skill to add broad OpenClaw bioinformatics capability or install selected categories for sequence analysis, RNA-seq, single-cell analysis, variant calling, metagenomics, structural biology, and related workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer gives one command broad, persistent authority to add hundreds of OpenClaw skills and run a secondary script from the cloned repository.

Mitigation: Install only after trusting the GPTomics bioSkills repository at the pinned commit, and review the cloned install-openclaw.sh before running it.

Risk: Installing the full collection may add more bioinformatics capabilities than a user needs.

Mitigation: Use --categories to install only the specific bioinformatics areas needed for the task.

Risk: The --uninstall option removes all bio-* skill directories from the OpenClaw skills directory.

Mitigation: Review the target skills directory before uninstalling and preserve any local bio-* skills that should not be removed.

## Reference(s):

- [ClawHub BioSkills listing](https://clawhub.ai/djemec/skills/bioskills)
- [bioSkills GitHub repository](https://github.com/GPTomics/bioSkills)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs, updates, or removes persistent OpenClaw bioinformatics skill directories after user execution.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
