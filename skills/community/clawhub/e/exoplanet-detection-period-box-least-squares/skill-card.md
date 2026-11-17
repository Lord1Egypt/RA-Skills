## Description:

Box Least Squares (BLS) periodogram guidance for detecting transiting exoplanets and eclipsing binaries in light curves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and astronomy analysts use this skill to run Astropy's Box Least Squares periodogram, tune period and duration searches, and validate candidate transit signals in photometric light-curve data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing required Python packages into a shared or privileged environment can affect unrelated projects.

Mitigation: Install Astropy, NumPy, Matplotlib, and optional preprocessing packages in a dedicated virtual environment without administrator privileges.

Risk: Coarse period grids, aliases, data gaps, or odd-even transit mismatches can produce misleading transit candidates.

Mitigation: Validate candidates with compute_stats(), odd-even checks, multiple observed transits, phase-folded plots, and refined period grids around promising peaks.

Risk: Aggressive preprocessing can remove or distort real transit-shaped signals.

Mitigation: Use preprocessing that preserves transit shapes and compare raw and cleaned light curves before relying on detections.

## Reference(s):

- [Astropy BLS Documentation](https://docs.astropy.org/en/stable/timeseries/bls.html)
- [Astropy Time Series Guide](https://docs.astropy.org/en/stable/timeseries/)
- [Kovacs, Zucker, and Mazeh (2002)](https://arxiv.org/abs/astro-ph/0206099)
- [Hartman and Bakos (2016)](https://arxiv.org/abs/1605.06811)
- [Lightkurve Tutorials](https://lightkurve.github.io/lightkurve/tutorials/)
- [Transit Least Squares](https://github.com/hippke/tls)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples operate on local light-curve data supplied by the user.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
