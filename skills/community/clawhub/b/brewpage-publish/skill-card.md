## Description: <br>
Publish HTML, markdown, text, files, or multi-file sites to brewpage.app and return an instant public URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kochetkov-ma](https://clawhub.ai/user/kochetkov-ma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to publish selected text, files, built static directories, or zip archives to brewpage.app for temporary public sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content to a public hosting service, which may expose files or text more broadly than intended. <br>
Mitigation: Use it only for content intended to become public, avoid secrets and private files, and review the selected content before upload. <br>
Risk: Broad invocation triggers may cause the skill to be selected for publishing requests where the user has not clearly chosen public hosting. <br>
Mitigation: Require an explicit confirmation step before calling brewpage.app and confirm namespace, password, TTL, and content type. <br>
Risk: Publishing a directory can accidentally include source files or generated artifacts. <br>
Mitigation: Publish built static output only and keep the documented exclusions for secrets, VCS data, dependencies, sourcemaps, logs, and editor files. <br>


## Reference(s): <br>
- [BrewPage homepage](https://brewpage.app) <br>
- [ClawHub listing](https://clawhub.ai/kochetkov-ma/brewpage-publish) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command blocks and a final public URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append a workspace-local brewpage-history.md file containing private owner tokens.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
