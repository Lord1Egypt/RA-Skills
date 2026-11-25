## Description:

Creates contact-sheet PNGs from FITS images, with selected header details, an optional sky-orientation compass, and an index of rendered or skipped files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Astronomers and observatory staff use FITS Peek to preview or triage observing images in contact sheets and trace each input to its output tile or skip reason. It supports quick visual review rather than measurement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, with unresolved local references and no applicable behavioral code analysis; its benign verdict does not establish that every installation source is risk-free.

Mitigation: Review the documented Git-based install source and skill before installing, as advised by the security guidance.

Risk: Large FITS images are rendered in memory without prior downsampling, and very high column counts can create large, slow sheets.

Mitigation: Use representative inputs and a modest column count, and allow enough memory and disk space for the generated sheets.

## Reference(s):

- [FITS Peek on ClawHub](https://clawhub.ai/raktikoo/skills/fitspeek)
- [Documented FITS Peek installation repository](https://github.com/RakTikoo/fitspeek)

## Skill Output:

**Output Type(s):** [PNG image files, CSV files]

**Output Format:** [PNG contact sheets and an index.csv file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contact sheets contain FITS image thumbnails; the CSV records each collected file's sheet, tile, render status, or skip reason.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
