## Description: <br>
Generates a structured Chinese AI news report from the past 24 hours and saves it to GetNote. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happyzengfen](https://clawhub.ai/user/happyzengfen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use this skill to collect recent AI news, filter for higher-value items, and publish a Markdown daily report to GetNote. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GetNote credentials are required for uploads and could be exposed if stored carelessly. <br>
Mitigation: Store GETNOTE_API_KEY and GETNOTE_CLIENT_ID locally with restricted file permissions and keep the .env file out of version control and logs. <br>
Risk: Generated reports may be uploaded to GetNote automatically, including when a cron schedule is enabled. <br>
Mitigation: Enable the cron job only when unattended daily network access and uploads are intended, and review the generated report workflow before scheduling it. <br>
Risk: AI news summaries can be incomplete, stale, or misleading if source search results are poor. <br>
Mitigation: Review source links and generated summaries before relying on or republishing the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happyzengfen/fengxinzi-ai-news) <br>
- [Publisher profile](https://clawhub.ai/user/happyzengfen) <br>
- [GetNote developer center](https://open.getnote.cn/) <br>
- [GetNote note save API endpoint](https://openapi.biji.com/open/api/v1/resource/note/save) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with shell setup and execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save generated reports to GetNote and may be scheduled by cron when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
