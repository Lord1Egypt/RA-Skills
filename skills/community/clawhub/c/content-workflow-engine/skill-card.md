## Description: <br>
Automates content creation, management, and distribution workflows for blogs, social media, newsletters, and publishing pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JacealLLC](https://clawhub.ai/user/JacealLLC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, marketing teams, agencies, and businesses use this skill to design and run repeatable content workflows for ideation, drafting, scheduling, publishing, distribution, and performance tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live publishing, scheduled posting, newsletter sending, or auto-response workflows can create externally visible actions. <br>
Mitigation: Review workflow definitions before execution, use test accounts first, and require explicit approval before any live external action. <br>
Risk: API credentials and other sensitive inputs may be exposed through workflow inputs or logs. <br>
Mitigation: Use least-privilege API keys, avoid passing secrets in workflow inputs, and inspect logs before sharing or storing them. <br>
Risk: Workflow execution includes under-scoped command execution behavior. <br>
Mitigation: Run only reviewed workflows in a controlled workspace and avoid executing untrusted workflow files. <br>


## Reference(s): <br>
- [Scheduled Blog Pipeline Guide](references/scheduled_blog.md) <br>
- [Multi-Platform Social Media Pipeline Guide](references/social_multi.md) <br>
- [Content Workflow Engine ClawHub Listing](https://clawhub.ai/JacealLLC/content-workflow-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON workflow definitions, and generated content or configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require API credentials and explicit approval before live publishing, scheduled posts, newsletter sends, or auto-responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
