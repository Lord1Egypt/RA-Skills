## Description: <br>
Ad creative search assistant that helps users search competitor ad creatives through AdMapix and returns results as H5 pages from api.admapix.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiwei199608](https://clawhub.ai/user/baiwei199608) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, ad intelligence users, and campaign analysts use this skill to turn natural-language ad research requests into confirmed AdMapix searches with filters for keyword, creative type, geography, dates, sorting, and pagination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ad search terms, regions, dates, and filters are sent to api.admapix.com. <br>
Mitigation: Avoid confidential client, campaign, or competitor terms unless sharing them with AdMapix is acceptable. <br>
Risk: Incorrectly parsed search parameters could send an unintended query. <br>
Mitigation: Review the displayed parameters before confirming each search. <br>
Risk: The skill requires an AdMapix API key. <br>
Mitigation: Configure the key through the platform setting and never print or expose the key value. <br>


## Reference(s): <br>
- [AdMapix website](https://www.admapix.com) <br>
- [AdMapix search API endpoint](https://api.admapix.com/api/data/search) <br>
- [Parameter Mapping Reference](references/param-mappings.md) <br>
- [ClawHub skill page](https://clawhub.ai/baiwei199608/admapix-1-0-13) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with confirmation prompts, configuration commands, and result links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are returned as generated H5 page links; the skill is instructed not to output inline result lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence); artifact metadata reports 1.0.13 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
