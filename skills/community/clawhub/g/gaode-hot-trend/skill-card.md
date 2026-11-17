## Description:

Supports user-directed, lightweight Gaode/Amap public-page lookups for nearby POIs, route summaries, coordinate-system notes, and simple reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to summarize public Gaode/Amap place and route information for travel planning, geodata labeling, and lightweight reporting. It should be used only for user-directed lookups that respect platform terms, rate limits, and verification controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation could be used to bypass CAPTCHA, human verification, rate limits, or other platform controls.

Mitigation: Keep use user-directed and lightweight; stop when verification or rate-limit controls appear and ask the user to continue through the normal site interface.

Risk: Bulk collection or interface reverse engineering could violate platform terms or scraping limits.

Mitigation: Use only public pages for limited information organization, avoid interface reverse engineering, and follow Gaode/Amap terms and crawler restrictions.

Risk: GCJ-02 and WGS-84 coordinate differences can cause location errors if coordinates are reused without context.

Mitigation: Label coordinate systems clearly and warn users to verify conversions before using coordinates for GPS or operational routing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/gaode-hot-trend)
- [Gaode/Amap Homepage](https://www.amap.com/)
- [Gaode/Amap Route Planning](https://www.amap.com/dir)
- [Gaode/Amap Place Search](https://www.amap.com/place)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown summaries, CSV-style tabular data, and coordinate-system notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links, report generation time, route details, POI attributes, and coordinate-system labels when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
