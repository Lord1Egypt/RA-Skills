## Description:

This is a summary the advantages and disadvantages of earthquake event detection and phase picking methods, shared by leading seismology researchers at the 2025 Earthquake Catalog Workshop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Seismology researchers, analysts, and developers use this skill to compare earthquake event detection and phase picking approaches such as STA/LTA, manual picking, deep learning pickers, and template matching for a seismic phase picking task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides scientific method-selection guidance that may be incomplete or unsuitable for a specific seismic network, dataset, or catalog quality target.

Mitigation: Treat outputs as reference guidance and have qualified seismology practitioners verify method choices, pick quality, and catalog results before operational use.

Risk: Automated phase picking approaches described by the skill can produce false detections, missed picks, or larger errors on out-of-distribution data.

Mitigation: Use validation datasets, appropriate thresholds, and manual review or refinement before relying on generated earthquake catalogs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/earthquake-phase-association-seismic-picker-selection)
- [Earthquake Catalog Workshop](https://ai4eps.github.io/Earthquake_Catalog_Workshop/)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown reference guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-facing method-selection guidance; it does not execute code, access data, or persist state.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
