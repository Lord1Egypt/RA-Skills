## Description: <br>
Provides real-time searches and verified Geekbench scores for the latest officially released flagship smartphones by brand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingqing404](https://clawhub.ai/user/dingqing404) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and device researchers use this skill to find current flagship smartphone releases, look up Geekbench results, and summarize benchmark distributions without relying on stale model knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can contact Geekbench and depend on live public web pages, so results may be incomplete or change over time. <br>
Mitigation: Confirm benchmark links and device release status before using the output for purchasing, publication, or comparison decisions. <br>
Risk: Helper scripts can write reports and raw data under a fixed local workspace path. <br>
Mitigation: Review or adjust output paths before running scripts in a shared, sandboxed, or production environment. <br>
Risk: The monitor script can delete old archive files in its configured archive directory. <br>
Mitigation: Back up or redirect the archive directory before enabling cleanup behavior. <br>
Risk: The monitor script can send a report to a fixed Feishu recipient through OpenClaw messaging. <br>
Mitigation: Verify the recipient and message content before running notification workflows. <br>


## Reference(s): <br>
- [ClawHub Geekbench release](https://clawhub.ai/dingqing404/geekbench) <br>
- [Geekbench Browser](https://browser.geekbench.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, textual summaries, JSON data files, and shell commands for optional helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include benchmark URLs, score statistics, device metadata, saved local report paths, and monitor notifications when helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
