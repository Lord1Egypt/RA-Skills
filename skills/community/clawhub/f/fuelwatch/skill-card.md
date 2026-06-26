## Description: <br>
Build, deploy, and extend the FuelWatch crowdsourced fuel availability tracker for South Africa. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to build, fix, deploy, and extend FuelWatch, a mobile-first web app for tracking fuel prices and availability at South African stations. It also guides planned backend, real-time, social sharing, WhatsApp, and voice-reporting extensions. <br>

### Deployment Geography for Use: <br>
South Africa <br>

## Known Risks and Mitigations: <br>
Risk: Applying deployment guidance to a live FuelWatch host could change files or restart the service unexpectedly. <br>
Mitigation: Confirm the target server and application path, review proposed changes first, and approve any service restart before execution. <br>
Risk: Future WhatsApp or voice-report ingestion could collect personal data or accept abusive and unverified reports. <br>
Mitigation: Add privacy, retention, validation, rate limiting, and abuse controls before enabling those channels. <br>
Risk: Crowdsourced fuel availability and price reports may be stale or inaccurate. <br>
Mitigation: Keep age-based unverified labels, add confirmation or upvote workflows, and avoid treating user reports as authoritative without review. <br>


## Reference(s): <br>
- [FuelWatch Backend Plan](references/backend-plan.md) <br>
- [FuelWatch live app](http://161.97.110.234:8080) <br>
- [ClawHub Fuelwatch listing](https://clawhub.ai/stefanferreira/fuelwatch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline code blocks and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include implementation plans, file-change guidance, deployment checks, and service restart commands for FuelWatch.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
