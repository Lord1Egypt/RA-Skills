## Description: <br>
This skill queries Douyin daily, weekly, and monthly TOP 50 account rankings, supports niche filtering, and generates Markdown summaries and HTML ranking reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brands, MCN teams, and industry analysts use this skill to identify high-performing Douyin accounts, compare niche rankings, monitor competitors, and generate shareable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and sends ranking query parameters to redfox.hk. <br>
Mitigation: Confirm the key source, scope, validity period, and revocation path before installation; store REDFOX_API_KEY only in the agent environment and do not expose it in prompts, logs, code, or output files. <br>
Risk: The skill can create recurring daily, weekly, or monthly ranking subscriptions. <br>
Mitigation: Create subscriptions only after explicit user confirmation, document the schedule, and verify how the user can view, pause, or cancel the task. <br>
Risk: The report generator writes local HTML files and attempts to open them automatically. <br>
Mitigation: Use trusted output paths and filenames, especially on Windows, and consider opening generated HTML reports manually after reviewing the file location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/douyin-top-account) <br>
- [RedFox publisher profile](https://clawhub.ai/user/redfox-data) <br>
- [Douyin ranking API documentation](references/api_docs.md) <br>
- [Category mapping](references/category_map.md) <br>
- [Score rules](references/score_rules.md) <br>
- [Update rules](references/update_rules.md) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown ranking tables, JSON data files, and HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY for RedFox API access; generated reports may include clickable Douyin profile links.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
