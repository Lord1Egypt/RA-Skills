## Description: <br>
Search Douyin for a user-specified topic and time range, then return the top hotspot videos ranked by visible engagement signals with strict no-fabrication rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eanpeng0-debug](https://clawhub.ai/user/eanpeng0-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, content operators, and topic researchers use this skill to find recent Douyin videos for a specified topic and time range, then review a ranked top-10 Markdown table based on visible engagement data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent opens Douyin pages and reads public result fields, which may expose browsing activity or fail when Douyin access is unavailable. <br>
Mitigation: Use the skill only when public Douyin browsing is acceptable, do not log in for this task, and return the documented failure structure when page access or browser capability is unavailable. <br>
Risk: Optional export can write collected results to local storage, including shared machines. <br>
Mitigation: Confirm the export path before saving, write only to the user-specified directory or default desktop location, and report export failures without discarding the visible results. <br>
Risk: Douyin engagement fields can be incomplete or change over time, so rankings may not match a platform-official or stable hotspot order. <br>
Mitigation: Use only visible fields, mark optional missing fields as missing, state the sorting basis, and avoid fabricating data or claiming an official ranking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eanpeng0-debug/douyin-topic-hotspot-collector) <br>
- [Publisher profile](https://clawhub.ai/user/eanpeng0-debug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown table with summary notes, or a structured Markdown failure report; optional exported result file when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks up to 10 Douyin results by visible likes first, with comments and collections as secondary signals; marks missing optional fields instead of fabricating data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
