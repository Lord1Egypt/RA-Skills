## Description: <br>
Monitor competitor product prices across Shopee, Lazada, Amazon, and others with automated tracking, alerts, and detailed comparison reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce sellers, dropshippers, and small business owners use this skill to track competitor product prices, compare pricing trends, and receive alerts when watched products cross configured thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep local records of competitor product URLs, prices, alerts, history, and reports. <br>
Mitigation: Confirm the stored file locations and data-retention expectations before enabling tracking, and delete saved monitoring data when it is no longer needed. <br>
Risk: Scheduled scans and external notifications can run repeatedly or send alerts to connected services. <br>
Mitigation: Confirm scan interval, destination service, and how to disable the cron job or notification route before enabling automation. <br>


## Reference(s): <br>
- [Platform-Specific Notes](references/PLATFORMS.md) <br>
- [Advanced Configuration](references/CONFIG.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ericlooi504/ericlooi504-gts-price-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, comparison tables, alert guidance, and optional CSV report instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local tracking, alert, history, and report files when the agent follows the skill workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
