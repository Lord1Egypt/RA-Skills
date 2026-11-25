## Description:

Converts observation times in CSV or FITS tables to BJD_TDB, requiring the input format, time scale, target coordinates, and observatory coordinates to be supplied explicitly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Astronomers and developers use this skill to convert observation time columns for exoplanet transit timing and other barycentric timing workflows. They supply the time format and scale, target coordinates, and observatory coordinates for the conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect time format or scale can silently shift converted times.

Mitigation: Set --format and --scale from authoritative input metadata, then inspect the printed time mapping and shift.

Risk: Incorrect observatory coordinates, including a plausible latitude and longitude swap, can produce plausible-looking results.

Mitigation: Enter site coordinates in latitude, longitude, height order and check the parsed site in the conversion summary.

Risk: Installation is documented from a GitHub repository, which requires trusting the package source.

Mitigation: Review the repository and install only from a source and release you trust.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/raktikoo/skills/bjd)
- [Project installation source listed in the skill](https://github.com/RakTikoo/bjd)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [CSV or FITS table with an appended bjd_tdb column, plus a conversion summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Carries through the input columns; output file type follows the .csv or .fits suffix.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
