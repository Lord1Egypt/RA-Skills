## Description:

Preprocessing and cleaning guidance for astronomical light curves prepared for period analysis, including outlier removal, trend removal, flattening, and data quality flag handling with lightkurve or general time series data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and astronomy data analysts use this skill to prepare raw light curves for period analysis and exoplanet transit detection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unpinned dependencies can reduce reproducibility or expose the workflow to supply-chain changes.

Mitigation: Install dependencies in a virtual environment and pin reviewed package versions when reproducibility or supply-chain control matters.

Risk: Aggressive preprocessing, incorrect quality flag interpretation, or overly short flattening windows can remove real transit signals.

Mitigation: Verify data quality flag conventions, choose preprocessing parameters appropriate to the target signal duration, and inspect before-and-after plots for each major step.

## Reference(s):

- [Lightkurve Preprocessing Tutorials](https://lightkurve.github.io/lightkurve/tutorials/index.html)
- [Removing Instrumental Noise](https://lightkurve.github.io/lightkurve/tutorials/2.3-removing-noise.html)
- [ClawHub Skill Page](https://clawhub.ai/wu-uk/skills/exoplanet-detection-period-light-curve-preprocessing)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes preprocessing cautions for quality flags, flattening windows, outlier thresholds, and visual verification.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
