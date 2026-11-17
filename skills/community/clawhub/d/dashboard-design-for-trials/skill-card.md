## Description:

Design dashboard layout sketches for clinical trials showing enrollment progress and adverse event rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, clinical operations teams, and trial reporting teams use this skill to generate HTML dashboard sketches for monitoring enrollment progress, adverse event rates, data quality metrics, and study milestones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can overwrite any writable output path supplied by the user.

Mitigation: Run it in a disposable workspace and choose an explicit output path that does not point to important files until output path restrictions and overwrite controls are added.

Risk: User-provided study names and IDs are embedded into generated HTML without escaping.

Mitigation: Use only trusted input values and review generated HTML before sharing it; add HTML escaping before using untrusted study metadata.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/dashboard-design-for-trials)

## Skill Output:

**Output Type(s):** [code, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with Python command examples and generated HTML file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a local HTML dashboard file from command-line study parameters; no external Python packages are required.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
