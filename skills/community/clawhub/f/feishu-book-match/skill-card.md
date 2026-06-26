## Description: <br>
Fills book match results (匹配结果) and Amazon links (书籍链接) in a Feishu Bitable by querying Amazon UK/US with ISBNs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JakLiao](https://clawhub.ai/user/JakLiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or operators maintaining Feishu book inventory tables use this skill to find Amazon listings by ISBN and batch-fill match status and product links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk Bitable updates can write incorrect match statuses or Amazon links at scale. <br>
Mitigation: Confirm the target table, field IDs, Feishu account, and Chrome profile, then run a small preview and review batches before continuing. <br>
Risk: Unattended background or cron execution can continue modifying records without timely review. <br>
Mitigation: Avoid unattended execution unless explicit limits, logs, stop conditions, and a recovery plan are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JakLiao/feishu-book-match) <br>
- [Publisher profile](https://clawhub.ai/user/JakLiao) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with inline JSON and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide Feishu Bitable updates and browser-based Amazon UK/US lookup steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
