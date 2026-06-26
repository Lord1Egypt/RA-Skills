## Description: <br>
Runs a self-contained Chinese and international AI news workflow for RSS capture, scheduled report generation, cumulative Excel outputs, and merged Word briefs inside the current workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nighmat1220](https://clawhub.ai/user/Nighmat1220) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, analysts, and developers use this skill to collect Chinese and international AI news from RSS sources, generate company-focused Excel reports, and create a daily Word brief. It supports capture-only, report-only, and full workflow runs in a workspace with the required source configuration and company list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feed configuration can include credentials and can disable TLS checks for arbitrary RSS sources. <br>
Mitigation: Run in a dedicated workspace, keep reusable secrets out of feed configs, use trusted HTTPS feeds with TLS verification enabled, and avoid verify_ssl=false. <br>
Risk: Collected content may be sent to the ARK model service during report generation. <br>
Mitigation: Use --disable-ai when collected content should not be sent to the model service. <br>


## Reference(s): <br>
- [Commands](references/commands.md) <br>
- [ClawHub skill page](https://clawhub.ai/Nighmat1220/ai-news-collection) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated workspace files include JSONL data, Excel workbooks, state files, snapshots, and Word briefs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ARK_API_KEY for model-generated summaries unless disable-AI mode is selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
