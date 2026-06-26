## Description: <br>
Discover and parse China's official holiday notices from gov.cn, normalize holiday and adjusted-workday rows, and apply low-frequency probing rules for future years. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyyyy0430](https://clawhub.ai/user/joeyyyy0430) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to build or explain China business calendars, sync official holiday schedules into storage, identify the first workday of a week, and implement holiday-aware weekly sending logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make web requests to official gov.cn pages and use a public-search fallback when official search is unavailable. <br>
Mitigation: Review network behavior before installation and prefer configured official notice URLs or China government policy search before fallback discovery. <br>
Risk: The skill may write small local cache or configuration entries for discovered notice URLs and probe history. <br>
Mitigation: Store source mappings and probe history separately, and review local cache paths and retention behavior before use. <br>
Risk: Holiday schedules for future years can be unavailable until an official notice is published. <br>
Mitigation: Do not fabricate future-year schedules; cache negative checks for the month and retry using the documented low-frequency probe window. <br>


## Reference(s): <br>
- [Official Notice Method](references/official-notice-method.md) <br>
- [China government policy search](https://sousuo.www.gov.cn/sousuo/search.shtml?code=17da70961a7&dataTypeId=107&searchWord=<query>) <br>
- [China State Council policy notice pages](https://www.gov.cn/zhengce/content/...) <br>
- [Skill page](https://clawhub.ai/joeyyyy0430/china-holiday-calendar-sync) <br>
- [Publisher profile](https://clawhub.ai/user/joeyyyy0430) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with JSON row examples and configuration patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce normalized holiday and adjusted-workday rows with date, is_holiday, is_workday, holiday_name, and source_url fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
