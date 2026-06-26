## Description: <br>
每日热榜技能 - 查询微博、知乎、B站、抖音等54个平台的热榜数据，支持定时推送和分类浏览。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[one-box-u](https://clawhub.ai/user/one-box-u) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to query current hot lists across Chinese social, video, news, technology, gaming, and culture platforms. It can also organize results by category, save local history, support personalized topic preferences, monitor keywords, and configure scheduled delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate DailyHotApi backend for public hot-list data. <br>
Mitigation: Review and deploy the backend deliberately, keep the API endpoint local or otherwise trusted, and configure DAILY_HOT_API_URL only after confirming the service you intend to query. <br>
Risk: Hot-list history and personalized preferences can be stored locally. <br>
Mitigation: Set DAILY_HOT_AUTO_SAVE=false or choose an appropriate DAILY_HOT_DATA_DIR when local retention is not desired, and periodically clear old data if retention is enabled. <br>
Risk: Scheduled delivery or Feishu push can send hot-list results to an unintended destination if misconfigured. <br>
Mitigation: Enable scheduled push only after confirming the destination, credentials, schedule, and disable procedure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/one-box-u/daily-hot-news) <br>
- [DailyHotApi project](https://github.com/imsyy/DailyHotApi) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown-formatted text with structured JSON-style data for hot-list results and configuration responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include platform names, rankings, heat values, item URLs, update times, saved-history summaries, topic filters, and delivery configuration status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
