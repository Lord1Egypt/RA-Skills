## Description: <br>
Parses CSV, JSON, Excel, Parquet, and SQL data files with encoding detection, common repair steps, conversion helpers, and data-cleaning utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuwenxi416488212-ship-it](https://clawhub.ai/user/qiuwenxi416488212-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and analysts use this skill to read, repair, clean, convert, and inspect common structured data files in agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote URL parsing can reach untrusted or internal network resources when parse_from_url is used without restrictions. <br>
Mitigation: Restrict or disable remote URL parsing in sensitive networks and allow only trusted external sources. <br>
Risk: Unpinned parser dependencies can change behavior or introduce supply-chain risk over time. <br>
Mitigation: Pin and review dependency versions before production use. <br>
Risk: Untrusted spreadsheets or Parquet files may exercise complex third-party parsers. <br>
Mitigation: Sandbox parsing jobs and avoid processing sensitive data without isolation and review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiuwenxi416488212-ship-it/data-parser-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/qiuwenxi416488212-ship-it) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce parsed tabular data, dictionaries, lists, converted files, validation errors, warnings, and retry guidance depending on the called parser utility.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
