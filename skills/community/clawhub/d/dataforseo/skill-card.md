## Description: <br>
Search Google and gather SEO data using the DataForSEO API for SERP results, keyword data, backlinks, on-page analysis, bulk lead generation, keyword research, rank tracking, and detailed SERP data at scale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and SEO operators use this skill to have an agent prepare DataForSEO API calls for Google SERP search, batch lead generation, Maps business lookup, keyword volume, backlink summaries, and site audit workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, business targets, locations, and site audit inputs are sent to DataForSEO. <br>
Mitigation: Avoid sending secrets, regulated data, or sensitive customer data in DataForSEO queries or audit targets. <br>
Risk: Bulk SERP and SEO workflows can incur paid DataForSEO API usage. <br>
Mitigation: Monitor API account usage, set operational limits where available, and review batch sizes before running high-volume requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/dataforseo) <br>
- [DataForSEO Google Organic Live Advanced Endpoint](https://api.dataforseo.com/v3/serp/google/organic/live/advanced) <br>
- [DataForSEO Google Organic Task Post Endpoint](https://api.dataforseo.com/v3/serp/google/organic/task_post) <br>
- [DataForSEO Google Locations Endpoint](https://api.dataforseo.com/v3/serp/google/locations) <br>
- [DataForSEO Google Maps Live Advanced Endpoint](https://api.dataforseo.com/v3/serp/google/maps/live/advanced) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with Python code examples and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD credentials; search inputs and site audit targets are sent to DataForSEO.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
