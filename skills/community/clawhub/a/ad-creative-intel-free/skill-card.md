## Description: <br>
A free ad intelligence helper for querying competitor creatives, campaign activity, and app store ranking changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, creative strategists, and market researchers use this skill to query ad creative search, app and developer insight, and app store ranking APIs, then receive raw JSON for their agent or workflow to analyze. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ad search keywords, competitor names, app identifiers, regions, and filters are sent to the third-party Ad Creative Intel API. <br>
Mitigation: Use the skill only for data your organization permits sharing with that service, and avoid confidential or personal data in queries. <br>
Risk: The API key could be exposed if pasted into prompts, committed to files, or printed in logs. <br>
Mitigation: Store ADC_INTEL_API_KEY in environment or platform secret storage, use a scoped key where possible, and do not echo or hardcode the key. <br>
Risk: Free-edition limits such as pageSize 10, no bulk export, and no historical trend or revenue/download endpoints may make results incomplete for larger research tasks. <br>
Mitigation: Paginate deliberately, disclose free-edition limits in downstream analysis, and avoid unsupported endpoints unless the user has upgraded access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ad-creative-intel-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Ad Creative Intel filter options endpoint](https://api.ad-creative-intel.com/api/data/filter-options) <br>
- [Ad Creative Intel search endpoint](https://api.ad-creative-intel.com/api/data/search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [Raw structured JSON with optional Markdown instructions and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ADC_INTEL_API_KEY; the free version limits pageSize to 10 and returns API fields without renaming or aggregation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
