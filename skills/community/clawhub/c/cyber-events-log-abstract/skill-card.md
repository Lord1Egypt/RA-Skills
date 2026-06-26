## Description: <br>
Generates concise summaries of XDR security-event aggregates, including trends, peak times, attack sources, victims, and risk-focused event tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoweijie](https://clawhub.ai/user/haoweijie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operations teams and developers use this skill to pull XDR event aggregates for a chosen time range and turn them into a concise Markdown security-event summary report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships with an embedded XDR API credential. <br>
Mitigation: Remove and rotate the bundled key before installation, then require a user-provided least-privilege credential. <br>
Risk: The release disables TLS verification for XDR requests. <br>
Mitigation: Restore TLS certificate verification and require users to configure the intended XDR endpoint. <br>
Risk: The release saves raw security-event data locally without clear upfront controls. <br>
Mitigation: Make raw-data persistence opt-in and document retention, file location, and access-control expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haoweijie/cyber-events-log-abstract) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/haoweijie) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown report with command-line execution guidance and optional local output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports a days parameter for the reporting window and an optional output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
