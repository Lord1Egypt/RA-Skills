## Description: <br>
Preprocessing and cleaning techniques for astronomical light curves, including outlier removal, trend removal, flattening, and data quality flag handling for period analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to prepare astronomical light curves for period analysis and exoplanet transit detection by applying quality filtering, outlier removal, detrending, and visualization checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aggressive filtering or detrending can remove real transit or periodic signals. <br>
Mitigation: Review preprocessing parameters, preserve transit shapes, and visually compare light curves before and after each major step. <br>
Risk: Quality flag conventions differ by data source and can invert which points are retained. <br>
Mitigation: Verify the data source's flag semantics before filtering and check that the resulting light curve is cleaner. <br>
Risk: Installing scientific Python dependencies from untrusted sources can introduce supply-chain risk. <br>
Mitigation: Install lightkurve, numpy, and matplotlib from trusted package sources in a virtual environment. <br>


## Reference(s): <br>
- [Lightkurve Preprocessing Tutorials](https://lightkurve.github.io/lightkurve/tutorials/index.html) <br>
- [Removing Instrumental Noise](https://lightkurve.github.io/lightkurve/tutorials/2.3-removing-noise.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/wu-uk/exoplanet-detection-period-light-curve-preprocessing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides parameter-selection guidance for light-curve preprocessing; does not execute analysis directly.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
