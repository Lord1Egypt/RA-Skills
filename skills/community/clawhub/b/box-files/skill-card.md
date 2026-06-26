## Description: <br>
Manage Box files, folders, collaborations, shared links, metadata, and enterprise content workflows via the Box API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and content operations teams use this skill to browse Box content, manage sharing and collaboration, inspect metadata, automate file workflows, and coordinate Box Sign signature requests through a connected Box account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OAuth-mediated access to the user's Box account through ClawLink. <br>
Mitigation: Install only if the user trusts ClawLink with the connected Box account, and review Box permissions during connection. <br>
Risk: Write, delete, sharing, user-management, legal-hold, and retention-policy actions can materially change Box content or enterprise policy. <br>
Mitigation: Use preview and explicit user confirmation before executing high-impact actions, and proceed only when the preview matches the intended target and effect. <br>
Risk: Tool availability and permissions depend on the connected Box account, enterprise policies, and the live ClawLink catalog. <br>
Mitigation: Verify the Box connection and current tool catalog before acting, and report real tool errors instead of inferring unsupported capabilities. <br>


## Reference(s): <br>
- [Box Developer Documentation](https://developer.box.com/) <br>
- [Box API Reference](https://developer.box.com/reference/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/box-files) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is based on the live ClawLink Box tool catalog after the user connects Box.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
