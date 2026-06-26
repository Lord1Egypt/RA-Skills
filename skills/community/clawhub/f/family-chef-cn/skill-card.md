## Description: <br>
为家庭规划一周菜单、搜索菜谱、计算营养、估算预算并生成购物清单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[villadora](https://clawhub.ai/user/villadora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking household cooks use this skill to plan weekly meals, search recipes, estimate nutrition and food budgets, and generate shopping lists based on family size, city, preferences, and dietary restrictions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores household profile details such as city, budget, food preferences, and dietary restrictions in a plaintext local file. <br>
Mitigation: Avoid entering sensitive information, review the saved profile before relying on it, and delete ~/.family-chef-profile.json when the profile is no longer needed. <br>
Risk: Recipe and price searches may send city, ingredient, or dish names to a web search provider. <br>
Mitigation: Do not include personal or sensitive details in search terms, and treat web search use as external disclosure of the query text. <br>
Risk: Nutrition and price estimates can be incomplete, stale, or unsuitable for a user's health needs or local market. <br>
Mitigation: Verify dietary guidance with qualified sources when health needs matter, and confirm prices before purchasing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/villadora/family-chef-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown conversation responses with meal plans, recipe guidance, nutrition and budget estimates, shopping lists, and optional local profile details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local plaintext profile data and web search results for recipe and price lookup.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
