## Description: <br>
外卖推荐技能。当用户提到"点外卖"、"外卖"、"订餐"、"叫外卖"、"推荐外卖"、"附近外卖"等关键词时自动触发。通过询问用户当前位置，综合大众点评、高德地图、美团、饿了么、京东外卖五大平台数据，搜索附近3km范围内支持堂食的优质外卖商家，按好评数量进行排名并推荐给用户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiezhenlin-tom](https://clawhub.ai/user/xiezhenlin-tom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to get nearby food-delivery recommendations based on location, meal time, platform ratings, dine-in availability, distance, price, and stated food preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves the user's address, dietary preferences, budget habits, and recent order history without clear opt-in, retention, or deletion controls. <br>
Mitigation: Review before installation; revise the skill to ask before saving personal details and to provide clear controls for disabling or deleting remembered data. <br>
Risk: Food-delivery recommendations may rely on public platform data that can be incomplete, stale, or missing current business and delivery status. <br>
Mitigation: Keep data-quality caveats in the output and ask users to confirm current ratings, hours, and delivery availability in the ordering app before placing an order. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiezhenlin-tom/food-delivery-recommend) <br>
- [Search Templates](references/search_templates.md) <br>
- [Ranking Criteria](references/ranking_criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown recommendation lists with ranked merchant summaries, caveats, and follow-up prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include restaurant names, cuisine, ratings, review counts, price, distance, business status, platform coverage, and data-quality warnings.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
