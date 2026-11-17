## Description:

Helps developers migrate from Google Maps Platform to AMap across REST APIs, JavaScript maps, and Android or iOS SDK integrations with mapping tables and code examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbs-amap](https://clawhub.ai/user/lbs-amap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan Google Maps to AMap migrations across web service APIs, JavaScript maps, and mobile SDK integrations. It helps choose Mainland or Non-Mainland endpoints, map request and response fields, and adapt code examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Non-Mainland geolocation examples may involve sensitive location or device identifiers over plaintext HTTP.

Mitigation: Do not send MAC addresses, IMEI, cell tower data, or precise location over plaintext HTTP; use HTTPS where supported and review geolocation examples before production use.

Risk: Copy-ready examples include shared public promotional API keys and mutable dependency or installation references.

Mitigation: Use dedicated restricted API keys for production and pin CLI, repository, Gradle, and CocoaPods versions in controlled environments.

## Reference(s):

- [Web Service API Parameter Mapping](artifact/references/web-api-params.md)
- [JS API Migration Reference](artifact/references/js-api-detail.md)
- [SDK Migration Reference](artifact/references/sdk-migration.md)
- [ClawHub Skill Page](https://clawhub.ai/lbs-amap/skills/amap-map-google-maps-migration)
- [AMap Overseas](https://mapsplatform.opnavi.com/)
- [AMap Developer Console](https://lbs.amap.com/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with API mapping tables and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects Mainland or Non-Mainland endpoints and web, JavaScript, or mobile migration guidance based on user input.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
