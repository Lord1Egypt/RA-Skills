## Description: <br>
ClawPulse connects an OpenClaw agent to a community analytics dashboard and pushes aggregate usage statistics without message content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pierreeurope](https://clawhub.ai/user/pierreeurope) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to install and configure ClawPulse, authenticate with GitHub, push aggregate usage metrics to a dashboard, and optionally schedule recurring pushes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may reuse and persist an existing GitHub token in a local ClawPulse config file. <br>
Mitigation: Prefer the dedicated ClawPulse device-flow setup with minimal scopes, and only allow token reuse when the user explicitly accepts the account-access risk. <br>
Risk: The skill configures recurring pushes of aggregate usage data to clawpulse.vercel.app. <br>
Mitigation: Confirm exactly what aggregate data is uploaded before enabling cron jobs, and disable scheduled pushes when ongoing collection is not desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pierreeurope/clawpulse) <br>
- [ClawPulse Dashboard](https://clawpulse.vercel.app) <br>
- [ClawPulse npm Package](https://www.npmjs.com/package/openclaw-pulse) <br>
- [ClawPulse Source Link](https://github.com/pierreeurope/clawpulse) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npx; may configure a local ClawPulse config file and OpenClaw cron jobs.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
