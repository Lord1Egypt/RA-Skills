## Description:

Collects Amap POI data for medical beauty and lifestyle beauty organizations by city keyword, then outputs raw JSON data and an optional Excel summary workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supperwk](https://clawhub.ai/user/supperwk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect district-level Amap POI records for selected Chinese cities and summarize medical beauty and lifestyle beauty organization counts and details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes a reusable Amap API key that should be treated as exposed.

Mitigation: Replace it with a user-owned, restricted key before installation or pass a key with --key or AMAP_KEY.

Risk: Generated Excel workbooks contain third-party POI text and may be opened in spreadsheet software with active content enabled.

Mitigation: Open generated XLSX files with external links and active content disabled, or use --skip-excel when workbook output is unnecessary.

Risk: The optional Excel export depends on openpyxl being installed in the runtime environment.

Mitigation: Install a pinned openpyxl version in a virtual environment before running Excel export.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supperwk/skills/amap-poi-fetch)
- [Amap district API endpoint](https://restapi.amap.com/v3/config/district)
- [Amap place text API endpoint](https://restapi.amap.com/v3/place/text)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Command-line progress text plus JSON files and optional XLSX workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes city-specific POI data under ~/.openclaw/workspace/data/<city>_poi/ and can skip Excel generation with --skip-excel.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
