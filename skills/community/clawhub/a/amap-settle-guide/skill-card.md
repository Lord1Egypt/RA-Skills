## Description:

Amap Settle Guide helps users choose commute-friendly rental areas by evaluating transit time, nearby amenities, rent value, specific listings, and rental search links from a workplace location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongdongyue](https://clawhub.ai/user/dongdongyue)

### License/Terms of Use:

MIT-0

## Use Case:

External users planning an internship, first job, job change, or move use this skill to compare where to live near a workplace. The skill guides an agent through AMap commute checks, amenity scoring, rent comparison, listing collection, and optional map or CSV output.

### Deployment Geography for Use:

Global, with practical coverage focused on cities and rental platforms supported by AMap and the referenced Chinese rental sites.

## Known Risks and Mitigations:

Risk: Generated HTML maps, CSV files, or shared reports may expose AMap API keys or detailed rental listing data.

Mitigation: Use restricted API keys for generated maps and review generated files before sharing them.

Risk: The skill may query AMap and scrape public rental listing sites, which can introduce third-party data and site-policy risk.

Mitigation: Use public data responsibly, respect relevant site terms and rate limits, and prefer reviewed outputs over unattended scraping.

Risk: Rental listings, commute times, and availability can change quickly, so recommendations may become stale.

Mitigation: Verify listings, prices, and commute routes directly before making housing decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongdongyue/skills/amap-settle-guide)
- [Publisher profile](https://clawhub.ai/user/dongdongyue)
- [Server-resolved GitHub source](https://github.com/dongdongyue/amap-settle-guide)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional CSV files and optional HTML map output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_API_KEY; optional AMAP_JSAPI_KEY and AMAP_SECURITY_JS_CODE support interactive HTML maps.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
