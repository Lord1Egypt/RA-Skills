## Description: <br>
Ads Execution Hub control skill for ad campaign management and optimization across Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, and DSP/programmatic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danyangliu-sandwichlab](https://clawhub.ai/user/danyangliu-sandwichlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Media teams and advertising operators use this skill to plan, launch, monitor, optimize, and scale campaigns across major ad platforms. It produces operator-facing bid, budget, testing, alerting, and handoff guidance tied to KPI constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Budget, bid, launch, scaling, or containment guidance could be applied directly to live advertising accounts without sufficient authorization or review. <br>
Mitigation: Treat outputs as recommendations and require an authorized operator to review them before making live ad platform changes. <br>
Risk: Incomplete campaign data, weak measurement confidence, policy flags, or account health issues could lead to poor optimization decisions. <br>
Mitigation: Request missing platform data, improve tracking before scaling, route policy or account blocks to the appropriate helper, and prefer containment actions when spend risk is severe. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danyangliu-sandwichlab/ads-execution-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with structured action plans, policies, test models, monitoring plans, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides recommendations for authorized operators to review before live platform changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
