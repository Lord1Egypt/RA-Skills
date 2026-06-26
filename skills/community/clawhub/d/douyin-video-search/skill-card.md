## Description: <br>
Searches Douyin videos through the TikHub API with keyword, pagination, sorting, and filtering options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Douyin videos by keyword, refine results by sort order, publication window, duration, and content type, and pass formatted or raw results into downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TikHub API token and sends Douyin search terms and filters to TikHub. <br>
Mitigation: Use a revocable or quota-limited token, and avoid sensitive names, secrets, internal project terms, or private investigative queries as keywords. <br>
Risk: Search output can include Douyin video links, creator names, and other content metadata returned by TikHub. <br>
Mitigation: Review results before storing or sharing them, and route raw JSON only to workflows that are approved to handle that data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ahsbnb/douyin-video-search) <br>
- [TikHub registration](https://user.tikhub.io/register) <br>
- [TikHub Douyin search API endpoint](https://api.tikhub.io/api/v1/douyin/search/fetch_general_search_v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text summaries or raw JSON from the TikHub API, with command-line invocation examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TikHub API token configured in ~/.openclaw/config.json or TIKHUB_API_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
