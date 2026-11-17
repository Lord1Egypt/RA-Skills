## Description:

Collects B2B foreign-trade leads from Google Maps for overseas distributors, wholesalers, buyers, and local businesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingfan0828](https://clawhub.ai/user/xingfan0828)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and export teams use this skill to collect overseas B2B lead lists from Google Maps after specifying an English product keyword, target region, and desired count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV export uses user-controlled keyword and region values in the filename.

Mitigation: Run the skill only in a controlled workspace and review generated filenames before sharing, moving, or opening outputs.

Risk: CSV rows contain untrusted third-party business data that may be unsafe for spreadsheet tools.

Mitigation: Treat generated CSV files as untrusted data and inspect or sanitize them before opening in spreadsheet software or distributing them.

Risk: Google Maps scraping may be rate-limited or blocked.

Mitigation: Use moderate target counts and avoid aggressive repeated runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xingfan0828/skills/foreign-trade-leads)
- [Publisher profile](https://clawhub.ai/user/xingfan0828)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Files]

**Output Format:** [Markdown guidance with bash commands and CSV output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV columns: name, phone, address, website, email.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
