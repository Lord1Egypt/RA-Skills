## Description: <br>
A temporary media hosting guide with seven-day retention, MIME validation, remote image fetching, upload handling, nginx configuration, cleanup, and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Byron-McKeeby](https://clawhub.ai/user/Byron-McKeeby) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and server administrators use this skill to set up and operate an ephemeral media-sharing endpoint for chat or collaboration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guidance can make real web-server changes to paths, nginx settings, permissions, logging, and cleanup schedules. <br>
Mitigation: Apply it only on the intended media-hosting server after reviewing and testing paths, permissions, nginx configuration, log retention, and cleanup timing. <br>
Risk: The remote fetch helper can retrieve user-supplied URLs and may be abused to access internal or private network destinations. <br>
Mitigation: Do not expose remote fetching to untrusted users until internal and private network destinations are blocked and abuse controls are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Byron-McKeeby/ephemeral-media-hosting) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with bash, nginx, PHP, cron, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes server setup, upload handling, cleanup, validation, monitoring, and operational guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
