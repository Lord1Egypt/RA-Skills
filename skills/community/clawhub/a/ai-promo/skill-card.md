## Description: <br>
查询大模型平台优惠信息，支持分类查询、订阅推送和提交优惠。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[destinyd](https://clawhub.ai/user/destinyd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up current large-language-model platform promotions by category, subscribe to daily promo pushes, and submit new promo links for review. It is intended for promo discovery and submission workflows backed by a remote promo service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a locally generated user ID and promo query or submission data to a remote promo service. <br>
Mitigation: Install only when this data flow is acceptable, and avoid submitting sensitive links or descriptions through the promo submission workflow. <br>
Risk: The skill persists local state in the user's home directory for user identity, subscriptions, and push logs. <br>
Mitigation: Review and remove ~/.promo_user_id, ~/.promo_subscribers.json, or ~/.promo_push.log when clearing local promo state or disabling the workflow. <br>
Risk: Daily push behavior can be enabled through cron-style scheduling and may continue until explicitly disabled. <br>
Mitigation: Enable push scheduling deliberately, review the subscription state, and disable the subscription or remove the scheduled job when the user no longer wants daily messages. <br>
Risk: User-submitted promo links may be reviewed and later shown to other users. <br>
Mitigation: Treat submitted promo URLs as public candidates, verify destinations before submission, and avoid submitting private or credential-bearing links. <br>


## Reference(s): <br>
- [AI Promo on ClawHub](https://clawhub.ai/destinyd/ai-promo) <br>
- [destinyd publisher profile](https://clawhub.ai/user/destinyd) <br>
- [AI Promo landing page](https://cli.aipromo.workers.dev/landing) <br>
- [AI Promo API endpoint](https://cli.aipromo.workers.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown-style promo listings, shell command invocations, and configuration guidance for subscription state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote promo service and local files for user ID, subscription state, and push logs.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
