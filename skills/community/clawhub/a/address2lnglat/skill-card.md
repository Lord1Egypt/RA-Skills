## Description:

Batch-converts place names and address keywords into BD-09 longitude and latitude coordinates using the Baidu Maps API, then saves the results as CSV and JSON files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggyybb](https://clawhub.ai/user/ggyybb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to collect candidate places from a search keyword, request BD-09 coordinates through Baidu Maps, and package the geocoding results for downstream mapping or data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, addresses, and the Baidu AK are sent to Baidu Maps.

Mitigation: Use the skill only with data and credentials approved for Baidu Maps, and avoid submitting sensitive location queries or credentials outside that policy.

Risk: The skill installs and runs Python dependencies and writes local output files.

Mitigation: Run it in a virtual environment, avoid privileged installs, and review generated CSV and JSON files before sharing or opening them in other tools.

Risk: Exported CSV files contain third-party API data that may be interpreted by spreadsheet software.

Mitigation: Treat exported CSV files as untrusted third-party data when opening them in spreadsheet applications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ggyybb/skills/address2lnglat)
- [Baidu Maps Open Platform](https://lbsyun.baidu.com/)
- [Baidu Place API endpoint](https://api.map.baidu.com/place/v2/search)
- [Baidu Geocoding API endpoint](https://api.map.baidu.com/geocoding/v3/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands plus generated CSV and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs BD-09 longitude and latitude rounded to 6 decimal places, with status, source, address, confidence, and type fields when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
