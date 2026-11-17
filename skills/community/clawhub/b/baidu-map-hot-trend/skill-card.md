## Description:

Helps agents use Baidu Maps for lightweight public POI lookup, route summaries, and BD-09 coordinate annotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather concise Baidu Maps public POI details, compare public transit and driving routes, and document BD-09 coordinate context for lightweight workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk scraping or workflows that violate Baidu Maps terms.

Mitigation: Use manual or lightweight queries, rate limit activity, and avoid reverse engineering or bulk collection.

Risk: Sensitive location tracking.

Mitigation: Limit use to public POI and route summaries, and avoid collecting or retaining sensitive movement or location data.

Risk: Coordinate-system mismatch can lead to inaccurate location interpretation.

Mitigation: Label BD-09 coordinates clearly and include conversion caveats when comparing them with GCJ-02 or WGS-84.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/baidu-map-hot-trend)
- [Baidu Maps](https://map.baidu.com/)
- [Baidu Maps Directions](https://map.baidu.com/direction)
- [Baidu Maps Search](https://map.baidu.com/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries with optional CSV-style tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Baidu Maps source links, report generation time, and BD-09 coordinate notes when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
