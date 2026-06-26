## Description: <br>
Finance Reporter Publish fetches public market prices from Yahoo Finance for major indexes, forex pairs, commodities, and Bitcoin, then prints a concise finance report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jfstylejf](https://clawhub.ai/user/jfstylejf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate market snapshot reports for tracked equity indexes, forex pairs, commodities, and Bitcoin using Yahoo Finance data. It can be run manually or scheduled after the user accepts outbound finance-data requests and separately configures any desired messaging integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Yahoo Finance for market data. <br>
Mitigation: Install and schedule it only in environments where outbound Yahoo Finance access is acceptable. <br>
Risk: Recurring cron execution can keep sending or generating reports after they are no longer needed. <br>
Mitigation: Add the cron job only for intended recurring use and remove it when the report is no longer required. <br>
Risk: DingTalk or WeChat delivery is described by the artifact but not fully implemented in the scanned behavior. <br>
Mitigation: Configure and verify any messaging integration separately before relying on pushed reports. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jfstylejf/finance-reporter-publish) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown report with optional shell commands for manual or scheduled execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and outbound access to Yahoo Finance; the artifact prints reports locally and messaging delivery requires separate configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
