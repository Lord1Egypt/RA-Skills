## Description:

Search Google and gather SEO data through the DataForSEO API for SERP results, keyword data, backlinks, on-page analysis, Maps business lookup, and high-volume lead generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to query DataForSEO for Google SERP results, keyword metrics, local business data, backlink summaries, and on-page SEO analysis at scale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, locations, and related query parameters are sent to DataForSEO.

Mitigation: Avoid using secrets, sensitive personal data, or regulated data unless external sharing with DataForSEO is approved.

Risk: DataForSEO API calls may incur pay-as-you-go charges.

Mitigation: Review pricing, batch sizes, and query volume before running generated requests.

Risk: The skill depends on DataForSEO account credentials in environment variables.

Mitigation: Store DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD securely and avoid printing or committing them.

## Reference(s):

- [DataForSEO Google Organic Live Advanced SERP endpoint](https://api.dataforseo.com/v3/serp/google/organic/live/advanced)
- [DataForSEO Google Organic Task Post endpoint](https://api.dataforseo.com/v3/serp/google/organic/task_post)
- [DataForSEO Google Organic Task Get Advanced endpoint](https://api.dataforseo.com/v3/serp/google/organic/task_get/advanced/{task_id})
- [DataForSEO Google SERP Locations endpoint](https://api.dataforseo.com/v3/serp/google/locations)
- [DataForSEO Google Maps Live Advanced endpoint](https://api.dataforseo.com/v3/serp/google/maps/live/advanced)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python code blocks and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD; generated examples call external DataForSEO API endpoints.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
