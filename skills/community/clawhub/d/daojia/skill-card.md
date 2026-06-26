## Description: <br>
Daojia helps agents summarize public JD Daojia merchant, product, activity, price, inventory, review, and delivery information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to inspect public JD Daojia merchant, product, and activity pages for lightweight shopping analysis, alerts, and comparisons without placing orders or using private account actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate too broadly for generic shopping requests. <br>
Mitigation: Use it only for JD Daojia-specific shopping or merchant and product page tasks, and review when it is invoked. <br>
Risk: Prices, inventory, delivery timing, and promotions can change by time and region. <br>
Mitigation: Include collection time, location or address context, and source links with summaries and comparisons. <br>
Risk: Using the skill for purchases, payments, logged-in account actions, reverse engineering, or bulk scraping would exceed the disclosed scope. <br>
Mitigation: Keep usage to lightweight analysis of public pages and avoid order placement, payment flows, private account actions, API calls, or bulk collection. <br>


## Reference(s): <br>
- [Daojia on ClawHub](https://clawhub.ai/CodeKungfu/daojia) <br>
- [JD Daojia homepage](https://www.jddj.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown summaries, comparison notes, and extracted public-page fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include collection time, region or address context, source links, and price or inventory caveats.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
