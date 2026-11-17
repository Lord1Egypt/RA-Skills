## Description:

Download water level, gage height, discharge, and station data from USGS with the Python dataretrieval NWIS package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and flood-risk workflows use this skill to retrieve USGS water-level, streamflow, and station metadata for specified stations and date ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned dataretrieval package can introduce unreviewed dependency changes.

Mitigation: Use a virtual environment and pin dataretrieval to a reviewed version for production or regulated workflows.

Risk: USGS requests can return empty data, connection errors, or rate limiting for large or unsupported requests.

Mitigation: Validate non-empty responses, handle exceptions, retry appropriately, and split large station or date-range requests into smaller batches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/flood-riREDACTED-SECRET)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes station ID, date range, USGS parameter-code, DataFrame-column, and retry guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
