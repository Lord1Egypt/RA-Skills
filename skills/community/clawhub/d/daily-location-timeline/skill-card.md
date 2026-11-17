## Description:

Reconstructs a day-by-day city and location timeline across multiple years from payment, travel, navigation, and photo GPS records, with evidence checks to correct location errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunerdao](https://clawhub.ai/user/sunerdao)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Individuals use this skill to organize payment records, travel tickets, GPS traces, bookings, and photo metadata into a reviewed daily location timeline for personal records or supporting documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inferred locations may replace evidence-backed locations in the resulting timeline.

Mitigation: Work on private copies, back up the baseline workbook before each run, and independently compare inferred days with original evidence before using the timeline for reimbursement or residency support.

Risk: GPS exports and intermediate files can expose sensitive location history.

Mitigation: Protect GPS exports and delete unnecessary intermediate files.

## Reference(s):

- [Standard operating procedure](artifact/references/sop.md)
- [Photo GPS method](artifact/references/photo_gps_method.md)
- [Travel legs schema](artifact/references/travel_legs_schema.md)
- [ExifTool](https://exiftool.org)
- [ClawHub skill listing](https://clawhub.ai/sunerdao/skills/daily-location-timeline)

## Skill Output:

**Output Type(s):** [Guidance, CSV, XLSX]

**Output Format:** [XLSX workbook and CSV daily timeline, with optional JSON GPS results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily locations are inferred from multiple evidence sources and should be reviewed against the original records.]

## Skill Version(s):

2.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
