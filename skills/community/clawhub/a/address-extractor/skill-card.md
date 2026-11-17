## Description:

Extracts, cleans, and standardizes Chinese address information from unstructured text, with optional AMap geocoding to return coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouyouwen](https://clawhub.ai/user/zhouyouwen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to turn customer records, orders, documents, and other unstructured Chinese text into standardized address components and, when configured, geographic coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Geocoding can send sensitive customer, logistics, or personal address queries to AMap when an API key is configured.

Mitigation: Use the extractor without an AMap API key for sensitive data unless consent and policy approval allow external geocoding.

Risk: Parsed or geocoded addresses may be inaccurate for important operational decisions.

Mitigation: Review standardized addresses and coordinate results before using them for routing, delivery, customer records, or other consequential workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhouyouwen/skills/address-extractor)
- [Address Extraction Reference](references/README.md)
- [Configuration Template](references/config_template.json)
- [AMap Open Platform](https://lbs.amap.com/)
- [AMap Geocoding API Endpoint](https://restapi.amap.com/v3/geocode/geo)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with Python snippets and JSON-like structured address results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional AMap geocoding output when an API key is configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
