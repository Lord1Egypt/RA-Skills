## Description: <br>
Runs the sports science crawler to generate a daily report, sync to Notion, and prevent duplicate content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w2478328197-arch](https://clawhub.ai/user/w2478328197-arch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run a local sports science update workflow that fetches recent research and wearable technology news, creates a daily Markdown report, syncs it to Notion, and tracks processed items to reduce duplicate content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python crawler from the sports-science-daily project and writes local report and history files. <br>
Mitigation: Install only if you trust the local project, review daily_sports_update.py and requirements.txt before running, and execute it from the intended directory. <br>
Risk: The workflow uses a Notion integration token and writes generated content to the configured Notion page. <br>
Mitigation: Use a Notion integration token scoped only to the target page and confirm NOTION_PAGE_ID points to the intended destination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/w2478328197-arch/generate-daily-sports-update) <br>
- [Project homepage](https://github.com/w2478328197-arch/sports-science-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, Notion credentials, and the local sports-science-daily project; the invoked script updates a local processed_history.json file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
