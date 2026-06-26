## Description: <br>
AI Topic Scout Feishu collects configured YouTube and Twitter/X content, analyzes AI topic trends and heat, and writes topic recommendations to Feishu Bitable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xdimtech](https://clawhub.ai/user/xdimtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, and developers use this skill to track configured AI-topic sources, aggregate cross-platform trends, score topic heat, and maintain a Feishu Bitable topic pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes analysis results to Feishu tables. <br>
Mitigation: Use a dedicated Feishu workspace or table, grant only the needed write access, and review sharing settings before recurring use. <br>
Risk: Configured YouTube, Twitter/X, and API-token sources can expose sensitive or unintended data if shared. <br>
Mitigation: Review configured sources, avoid private or sensitive accounts, and keep API keys and bearer tokens out of shared configuration files. <br>
Risk: Optional cron automation can repeatedly fetch external content and write new table records. <br>
Mitigation: Enable cron only when recurring fetches are intended, set conservative schedules, and periodically inspect the generated records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xdimtech/ai-topic-scout-feishu) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries, YAML configuration examples, shell command examples, and Feishu Bitable records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write records to Feishu Bitable and invoke local fetch scripts when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
