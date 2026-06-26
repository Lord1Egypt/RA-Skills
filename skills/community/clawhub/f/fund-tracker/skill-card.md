## Description: <br>
Tracks fund purchase availability, daily purchase quotas, fees, and changes since the previous run using local AKShare-based presets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alondotsh](https://clawhub.ai/user/alondotsh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check whether configured funds are open, quota-limited, paused, or changed since the previous check. It is intended for fund purchase status tracking, not stock or ETF market-price analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fund status results depend on AKShare and the upstream Eastmoney data source, so network failures or schema changes can produce errors or stale results. <br>
Mitigation: Treat output as informational, review JSON errors, and verify important fund status results against an authoritative source before acting. <br>
Risk: The skill stores local runtime history under the skill directory to detect changes between runs. <br>
Mitigation: Keep generated runtime history out of version control and review it before sharing the skill directory. <br>
Risk: The Python dependency stack fetches public fund data and should not be treated as financial advice. <br>
Mitigation: Install dependencies in a controlled environment and use the results only as fund-status tracking input, not investment guidance. <br>


## Reference(s): <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/alondotsh/fund-tracker) <br>
- [Publisher Profile](https://clawhub.ai/user/alondotsh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command output summarized from JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local preset configuration and runtime history files inside the skill directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
