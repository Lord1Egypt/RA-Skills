## Description: <br>
Enriches leads by finding contact emails through contact pages, Instagram, Hunter.io, and email patterns, then formats deduplicated records for Notion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[visualdeptcreative](https://clawhub.ai/user/visualdeptcreative) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, growth, and operations teams use this skill to enrich lead records with candidate contact emails and prepare clean, deduplicated lead data for Notion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead domains are sent to Hunter.io and enriched results may contain contact information. <br>
Mitigation: Use a scoped Hunter.io API key, process only authorized leads, and delete retained workspace data when it is no longer needed. <br>
Risk: Notion sync can expose or duplicate lead data if access is too broad or deduplication is skipped. <br>
Mitigation: Grant Notion access only to the intended lead pipeline and normalize domain_key before checking for existing records. <br>
Risk: Email pattern guessing can produce incorrect contacts. <br>
Mitigation: Prefer direct sources and Hunter.io results above 70% confidence, retain email source and confidence fields, and review records before outreach. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/visualdeptcreative/data-enricher) <br>
- [Hunter.io domain search endpoint](https://api.hunter.io/v2/domain-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [JSON lead records with concise status text and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batches 10 leads at a time, limits Hunter.io lookups to 10 per session with 5 seconds between API calls, and saves formatted batches as workspace/leads-enriched-YYYY-MM-DD.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
