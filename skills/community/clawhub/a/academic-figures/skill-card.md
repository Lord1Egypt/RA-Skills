## Description:

Generates publication-ready scientific figures from data with a single command, including statistical charts, journal presets, and exports in common publication formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docsor1212](https://clawhub.ai/user/docsor1212)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use the skill to turn JSON, CSV, or Excel data into static figures for papers and journal submissions, including batch re-rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags shell execution in the test suite and an installation source that can change.

Mitigation: Review test commands and pin and inspect the source revision before running installation or test commands.

Risk: Reproduction bundles may contain original data, and the security analysis was partial.

Mitigation: Inspect bundles and remove sensitive or identifying data before sharing; review areas the scan did not analyze before use.

Risk: Automated figure validation may not catch every issue that matters for a submission.

Mitigation: Check figures against the source data and the target journal's requirements before submission.

## Reference(s):

- [Academic Figures release page](https://clawhub.ai/docsor1212/skills/academic-figures)
- [Quickstart guide](artifact/references/quickstart.md)
- [Chart limits and compatibility](artifact/references/limits.md)
- [Python API guide](artifact/references/python-api.md)

## Skill Output:

**Output Type(s):** [Image files, PDF documents, JSON configurations, Shell commands, Python code]

**Output Format:** [PNG, TIFF, PDF, SVG, and EPS figures; JSON specifications, Python API calls, and command-line instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static figures; chart type and export format depend on the supplied data and options.]

## Skill Version(s):

8.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
