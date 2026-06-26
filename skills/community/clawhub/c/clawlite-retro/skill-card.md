## Description: <br>
ClawLite Retro helps developers generate engineering retrospectives from local Git history, code-change metrics, contributor activity, file hotspots, and TODO backlog signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review recent repository work over 24-hour, 7-day, 14-day, or 30-day windows and produce a data-backed retrospective with contributor feedback and next-step guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The retrospective may expose contributor names, email addresses, work timing, file hotspots, and TODO or backlog details from the repository. <br>
Mitigation: Use it only in repositories where that project activity data is appropriate to inspect and share with the intended audience. <br>
Risk: The skill may use existing Git remote credentials when fetching repository history. <br>
Mitigation: Run it in trusted repository workspaces and review the target remote before invoking the retro workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/clawlite-retro) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown retrospective with tables, histograms, ranked lists, and contributor sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts /retro with optional 24h, 7d, 14d, or 30d windows and uses local Git data for the report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
