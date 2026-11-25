## Description:

Turn a folder tree of telescope FITS files into one night-log CSV with header keywords normalised across instruments (EXPTIME/EXPOSURE/EXPT, OBJECT/TARGET/OBJNAME and more), plus an audit flagging corrupt files, missing fields, duplicated keywords and headers with no WCS. Use when asked to build a night log, catalogue or inventory a folder of FITS files, summarise an observing night, or check FITS headers for problems. Not for rendering FITS files as contact-sheet images (use fitspeek), converting observation times to BJD_TDB (use bjd), or cross-matching catalogues (use epochmatch).

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT

## Use Case:

Astronomers and telescope data users can scan an observing-night folder to create a consistent FITS-header log and identify files with missing or problematic metadata. The audit helps review data quality before analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan had partial coverage and its clean verdict is informative rather than a guarantee of safety; installation retrieves the project from GitHub.

Mitigation: Review the source and dependencies before installation, and treat the scan verdict as one signal.

## Reference(s):

- [FITS Log on ClawHub](https://clawhub.ai/raktikoo/skills/fitslog)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [CSV files and a plain-text scan summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The night log contains one row per FITS file; an optional audit CSV contains one row per finding.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
