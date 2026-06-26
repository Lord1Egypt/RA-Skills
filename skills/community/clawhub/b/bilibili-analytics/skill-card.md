## Description: <br>
Searches public Bilibili video results for a keyword, extracts video metadata, and generates statistical reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcjinglang](https://clawhub.ai/user/pcjinglang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and social media analysts use this skill to collect public Bilibili search-result metadata for a keyword and produce Markdown statistics reports about authors, posting dates, play counts, and comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Bash/Python scripts and an external browser automation tool. <br>
Mitigation: Review the scripts before execution, confirm agent-browser is installed, and use modest page counts. <br>
Risk: Reports are based on public Bilibili pages whose contents can change over time. <br>
Mitigation: Treat generated analysis as a snapshot of the collection time rather than a permanent dataset. <br>
Risk: The skill creates local JSON and report files. <br>
Mitigation: Run it in a working directory where generated files can be reviewed, retained, or removed intentionally. <br>


## Reference(s): <br>
- [Usage Examples](references/usage-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/pcjinglang/bilibili-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and JSON data files, with shell commands for browser scraping and analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local data and report files from public Bilibili search pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
