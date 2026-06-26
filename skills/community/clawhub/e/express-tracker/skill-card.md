## Description: <br>
Express Tracker helps agents generate Kuaidi100 tracking links for major Chinese courier services, with automatic carrier detection and single-package or batch workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang-junjian](https://clawhub.ai/user/wang-junjian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to identify likely courier carriers from tracking numbers and generate Kuaidi100 query links for individual shipments or batches without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracking numbers are embedded in Kuaidi100 query links and may be sent to an external website when opened. <br>
Mitigation: Use browser opening only when sharing the tracking number with Kuaidi100 is acceptable. <br>
Risk: User-selected output paths can overwrite existing files. <br>
Mitigation: Choose output paths deliberately and review existing files before writing results. <br>
Risk: The scripts include a hard-coded local Python import path that can reduce portability in shared or production environments. <br>
Mitigation: Fix the import path or run the scripts from a controlled skill directory before relying on them operationally. <br>


## Reference(s): <br>
- [Express Tracker on ClawHub](https://clawhub.ai/wang-junjian/express-tracker) <br>
- [Kuaidi100 tracking query](https://www.kuaidi100.com/chaxun?nu={tracking_number}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files] <br>
**Output Format:** [Plain text, JSON, or Markdown tracking summaries with Kuaidi100 query URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write results to a user-selected file and can open a query URL in the browser when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
