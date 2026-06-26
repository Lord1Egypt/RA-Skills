## Description: <br>
通过 Clawec API 跟踪亚马逊新品发布与排行，可按类目筛选。在用户需要亚马逊新品跟踪、New Releases 监控、类目新品榜、选品发现、新品趋势调研时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users and ecommerce operators use this skill to query ClawEC for Amazon New Releases data by category, then summarize new products, rankings, prices, ratings, links, and follow-up product research signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A ClawEC API key is required and could be exposed if pasted into prompts, shell history, or shared logs. <br>
Mitigation: Store CLAWEC_API_KEY in environment or secret storage, avoid embedding it in files, and rotate the key if it is exposed. <br>
Risk: Category queries and the API key are sent to ClawEC when the skill performs lookups. <br>
Mitigation: Use the skill only when sharing the selected Amazon category with ClawEC is acceptable, and do not pass unrelated sensitive text as the category argument. <br>
Risk: The ClawEC API response data fields may vary, so rigid downstream parsing could omit or mislabel product details. <br>
Mitigation: Validate the response shape before acting on results and present uncertain or missing fields as unavailable rather than inferred. <br>


## Reference(s): <br>
- [Response schema](references/response-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/anyunzhong/clawec-amazon-new-release) <br>
- [ClawEC API base URL](https://www.clawec.com/api) <br>
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are based on the live ClawEC API response, whose data fields may vary by request.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
