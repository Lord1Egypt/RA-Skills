## Description: <br>
Box Least Squares (BLS) periodogram for detecting transiting exoplanets and eclipsing binaries. Use when searching for periodic box-shaped dips in light curves. Alternative to Transit Least Squares, available in astropy.timeseries. Based on Kovacs et al. (2002). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and astronomy analysts use this skill for guidance on applying Astropy's BoxLeastSquares periodogram to light curves, selecting period and duration grids, and validating candidate transits or eclipsing binaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BLS candidate detections can be misleading when preprocessing, period grids, duration ranges, or aliases are poorly chosen. <br>
Mitigation: Validate candidates with depth SNR, odd-even depth comparison, transit count, phase-folded plots, and follow-up checks around promising periods. <br>
Risk: Generated examples may include dependency installation commands or file-loading code that should be adapted to the user's environment. <br>
Mitigation: Review commands, package versions, local file paths, and data columns before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wu-uk/exoplanet-detection-period-box-least-squares) <br>
- [Astropy BLS Documentation](https://docs.astropy.org/en/stable/timeseries/bls.html) <br>
- [Astropy Time Series Guide](https://docs.astropy.org/en/stable/timeseries/) <br>
- [Kovacs, Zucker, and Mazeh (2002)](https://arxiv.org/abs/astro-ph/0206099) <br>
- [Hartman and Bakos (2016)](https://arxiv.org/abs/1605.06811) <br>
- [Lightkurve Tutorials](https://lightkurve.github.io/lightkurve/tutorials/) <br>
- [Transit Least Squares](https://github.com/hippke/tls) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dependency installation commands, Astropy usage examples, validation criteria, and interpretation guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
