## Description: <br>
Submit Dataify Google Map Details Builder tasks for four Google Maps detail collection modes by URL, CID, location, or place ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and submit Dataify Builder jobs that collect Google Maps detail records by URL, CID, location search, or place ID. The skill returns task identifiers, status information, and guidance for viewing results in Dataify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted Google Maps URLs, CIDs, place IDs, keywords, coordinates, and task parameters are sent to Dataify for processing. <br>
Mitigation: Review all task parameters before submission and avoid sensitive customer or business lists unless Dataify's handling is acceptable for the intended use. <br>
Risk: Saving DATAIFY_API_TOKEN locally makes the credential available to future runs in that environment. <br>
Mitigation: Save the token locally only after explicit user confirmation and only in environments where future access to that credential is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-google-map-details) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>
- [Google country values](references/google_countries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with parameter tables, shell command examples, and JSON task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Dataify task_id, status, selected mode, spider_id, normalized parameters, file_name, dashboard_url, and message when the submission succeeds.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
