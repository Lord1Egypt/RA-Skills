## Description: <br>
Run and monitor PapersFlow DeepScan jobs for long-running research progress, intermediate findings, final reports, and plotting from completed runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[papersareflowing](https://clawhub.ai/user/papersareflowing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage asynchronous PapersFlow DeepScan research jobs, monitor live progress, summarize intermediate and final findings, and create plots only after report data is stable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DeepScan jobs and stored reports may send research prompts or report data to the configured PapersFlow service. <br>
Mitigation: Avoid sensitive material unless that sharing is intended, and confirm the data-sharing posture before starting a run. <br>
Risk: Long-running DeepScan jobs are asynchronous and may not provide automatic completion notifications. <br>
Mitigation: Poll deliberately with live snapshots or lightweight status checks and keep the next action clear when the report is not ready. <br>
Risk: Plots generated from sparse or unstable report data may be misleading. <br>
Mitigation: Generate plots only after final or stable report data is available and the dataset is meaningful for visualization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/papersareflowing/deepscan-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/papersareflowing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown status updates, summaries, and plotting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live progress, top papers, key findings, final report summaries, and plot recommendations when completed report data supports them.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
