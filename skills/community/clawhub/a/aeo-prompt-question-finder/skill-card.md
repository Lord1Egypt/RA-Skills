## Description: <br>
Finds question-based Google Autocomplete suggestions for a seed topic by prepending question modifiers, supporting AEO prompt research, content ideation, and topic question discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, marketers, SEO/AEO researchers, and content teams use this skill to discover question-style search suggestions for a topic and optionally enrich the suggestions with search volume. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search topics are sent to Google Autocomplete when the skill is run. <br>
Mitigation: Use the skill only with topics that are appropriate to share with Google Autocomplete. <br>
Risk: The optional --volume mode reads DataForSEO credentials and sends keyword lists to DataForSEO. <br>
Mitigation: Enable --volume only intentionally, prefer dedicated DataForSEO credentials, and avoid sending sensitive keyword lists. <br>
Risk: High-volume or parallel autocomplete requests may trigger temporary IP blocks. <br>
Mitigation: Use the documented --delay option, especially for batch runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/psyduckler/aeo-prompt-question-finder) <br>
- [Google Autocomplete endpoint](https://suggestqueries.google.com/complete/search) <br>
- [DataForSEO Google Ads search volume endpoint](https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown-style console output or JSON keyed by question modifier.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional DataForSEO enrichment can add monthly search volume values when credentials are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
