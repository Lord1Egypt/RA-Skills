## Description: <br>
登录 Alpha派并抓取最近 N 小时点评，保存原文、结构化归档并建立本地索引；也可以用精确检索、向量检索或混合检索查询最近 N 天的历史点评库并生成手机友好摘要，可选发送到飞书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdbotrr](https://clawhub.ai/user/clawdbotrr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and agents use this skill to collect recent AlphaPai market comments, archive them locally, query the comment history by topic and time window, and generate concise mobile-friendly summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse AlphaPai login sessions or account credentials. <br>
Mitigation: Use a dedicated AlphaPai token or site-specific cookies where possible, avoid full browser profiles for shared releases, and rotate or remove credentials when no longer needed. <br>
Risk: Scraped authenticated AlphaPai content is stored locally in raw files, normalized archives, indexes, reports, and runtime metadata. <br>
Mitigation: Keep the output directory access-controlled and periodically delete storage-state, cookie backup, raw, index, report, and runtime files that are no longer required. <br>
Risk: Summaries or derived content may be sent to external services such as Feishu webhooks or an AI model. <br>
Mitigation: Keep Feishu disabled unless transmission is intended and review configured model or webhook destinations before processing sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawdbotrr/alphapai-scraper) <br>
- [AlphaPai web application](https://alphapai-web.rabyte.cn) <br>
- [AlphaPai comment page](https://alphapai-web.rabyte.cn/reading/home/comment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON archives, SQLite and vector indexes, local runtime files, and optional Feishu webhook messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written under the configured local data directory and may include raw scraped content, normalized records, reports, and runtime metadata.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
