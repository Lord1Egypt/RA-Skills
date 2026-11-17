## Description:

Build the patent-data layer for an applicant asset dashboard using PatSnap search and analytics APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

IP analysts, developers, and external teams use this skill to retrieve applicant patent portfolios and prepare dashboard-ready patent analytics, including patent-type subsets, filing trends, classification distribution, filing-office coverage, top inventors, and word-cloud data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PatSnap API credentials could be exposed if passed insecurely or logged.

Mitigation: Use a narrowly scoped PatSnap API key through PATSNAP_API_KEY or a secret manager, and avoid embedding or logging real keys.

Risk: Untrusted applicant names could produce misleading or unsafe query behavior.

Mitigation: Validate or escape applicant-name input before sending it to PatSnap APIs.

Risk: Unavailable or changed PatSnap endpoints can make dashboard counts unreliable.

Mitigation: Verify current PatSnap endpoint availability and schemas before production use, and mark unavailable panels as data unavailable rather than fabricating values.

## Reference(s):

- [PatSnap Authentication Guide](https://open.patsnap.com/devportal/guides/authentication)
- [P002 Patent Query Search Endpoint](https://connect.patsnap.com/search/patent/query-search-patent/v2)
- [P003 Analytics Query Search and Filter](https://open.patsnap.com/devportal/api-reference/patent-field/query)
- [P072 Classification Search Assistant](https://open.patsnap.com/devportal/api-reference/search/patent/classification/helper-search)
- [P066 Patent Classification Description](https://open.patsnap.com/devportal/api-reference/high-value-data/patent-classification-description)
- [A006 Top Inventors](https://open.patsnap.com/devportal/api-reference/insights/inventor-ranking)
- [A002 Innovation Word Cloud](https://open.patsnap.com/devportal/api-reference/insights/word-cloud-query)
- [API call notes](references/api_notes.md)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/build-patent-asset-dashboard-ip)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with JSON request examples and Python helper code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PatSnap Open Platform API key and endpoint availability checks before relying on returned counts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
