## Description: <br>
自动获取财联社电报自定义关键词新闻并格式化为一句话新闻。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FrankLe1117](https://clawhub.ai/user/FrankLe1117) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to search 财联社 telegraph news by custom keyword and receive concise, categorized one-sentence news summaries. It can also support optional scheduled news runs when the user explicitly enables the provided cron configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install the agent-browser dependency during ordinary use. <br>
Mitigation: Install agent-browser manually through a trusted path before using the skill, or review the install step before allowing it to run. <br>
Risk: Broad trigger phrases may start browsing or dependency installation unexpectedly. <br>
Mitigation: Use explicit 财联社-related prompts and review the skill triggers before deployment. <br>
Risk: The optional cron block can create scheduled automatic runs. <br>
Mitigation: Enable the cron configuration only when scheduled 财联社 news retrieval is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FrankLe1117/cls-custom) <br>
- [财联社电报](https://www.cls.cn/telegraph) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown news summary with optional shell command and cron configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs concise factual summaries grouped by topic; browser access and network availability are required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
