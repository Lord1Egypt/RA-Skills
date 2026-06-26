## Description: <br>
Fetches CCTV Xinwen Lianbo content and saves the extracted program link, chapter summaries, and video links to a dated local text file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kawayixixing](https://clawhub.ai/user/kawayixixing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill to retrieve the daily CCTV Xinwen Lianbo page, extract available video links and chapter summaries, and save them for local reading or archival workflows. It can also guide scheduled execution on Windows, Linux, Unix, or macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script contacts CCTV web pages during execution. <br>
Mitigation: Run it only where outbound access to CCTV is acceptable and expected. <br>
Risk: The script creates or overwrites a dated text file in its script folder. <br>
Mitigation: Run it as a normal user in a directory where that write behavior is acceptable. <br>
Risk: Scheduled execution can repeatedly fetch network content and write local files. <br>
Mitigation: Configure cron, launchd, or Windows Task Scheduler only when automatic daily execution is intended. <br>


## Reference(s): <br>
- [Skill usage instructions](references/使用说明.md) <br>
- [CCTV Xinwen Lianbo page](https://tv.cctv.com/lm/xwlb/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus a dated UTF-8 text file containing Markdown-style links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes cctv_news_YYYYMMDD.txt in the script directory and prints basic status or error messages to the console.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
