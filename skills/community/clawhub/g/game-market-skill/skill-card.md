## Description: <br>
Query YY game trading marketplace listings by game and category; guides users to the website for actual buy/sell actions <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-lin](https://clawhub.ai/user/arc-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to browse YY game trading listings by game and category, paginate results, and open YY pages for buy or sell actions after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries YY marketplace listings and can send selected game and category search context to YY. <br>
Mitigation: Use it only when comfortable sharing that search context, and verify item details and URLs before acting on a listing. <br>
Risk: The skill can hand off buy or sell actions to the YY website, where purchases, sales, login, and payment are outside the agent. <br>
Mitigation: Complete any login, purchase, sale, or payment manually on the YY website after confirming the destination page. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/arc-lin/game-market-skill) <br>
- [YY marketplace](https://mall.yy.com?pageId=20000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with listing summaries, links, confirmation prompts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include direct links to YY listing detail pages and prompts before opening external marketplace pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
