## Description: <br>
电商竞品价格监控系统会帮助代理定时检查竞品商品页面，记录价格、库存和促销变化，并在变化超过阈值时提醒用户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijinhao123-dot](https://clawhub.ai/user/lijinhao123-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers, operators, brands, and price-sensitive shoppers use this skill to configure competitor product monitoring, compare collected prices over time, and request alerts or reports when prices, stock, or promotions change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled checks can repeatedly access ecommerce pages and may conflict with site terms, rate limits, or user expectations. <br>
Mitigation: Confirm product URLs, monitoring interval, thresholds, and retention expectations before enabling checks; prefer conservative intervals such as 30 minutes or longer. <br>
Risk: The skill may save screenshots and page data from monitored product pages. <br>
Mitigation: Avoid logged-in or private pages unless the user has explicitly approved saving that data, and confirm where screenshots and history files will be stored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijinhao123-dot/ecommerce-competitor-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/lijinhao123-dot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, alert text, saved monitoring data, screenshots, and report tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create scheduled checks and store baseline or history data when the host agent provides browser, cron, and file tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
