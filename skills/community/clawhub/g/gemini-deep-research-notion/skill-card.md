## Description: <br>
Triggers Gemini Deep Research through a browser session, waits for completion, extracts the report, and creates a formatted Notion page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PalmPalm7](https://clawhub.ai/user/PalmPalm7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a Gemini Deep Research workflow from an OpenClaw browser session and archive the resulting report in Notion. It is intended for users who have a logged-in Gemini account and a configured Notion integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Gemini browser session and use a local Notion API key to create pages. <br>
Mitigation: Review before installing, confirm the browser and Notion access are acceptable, and use a least-privilege Notion integration token shared only with the intended page. <br>
Risk: Research topics and full reports may be stored in Gemini, Notion, and an intermediate /tmp Markdown file. <br>
Mitigation: Avoid sensitive research topics unless that storage is acceptable, or edit the workflow to change storage behavior before use. <br>
Risk: The artifact includes a hard-coded Notion parent page ID and prepends a Chinese-language instruction to research queries. <br>
Mitigation: Replace the Notion parent page ID with the user's own destination and edit the language instruction if Chinese output is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PalmPalm7/gemini-deep-research-notion) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown report text, Notion page content, shell/API commands, and a final text summary with the Notion page URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Chinese-language research report unless the skill prompt is edited; may write an intermediate Markdown file under /tmp before exporting to Notion.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
