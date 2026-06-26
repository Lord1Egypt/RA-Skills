## Description: <br>
Helps agents create and manage Alibaba Cloud IMS video translation jobs through OpenAPI, including subtitle, voice, face processing, status polling, and job management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide Alibaba Cloud IMS video translation workflows, including preparing OSS inputs and outputs, submitting translation jobs, polling status, and managing jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide billable Alibaba Cloud video translation jobs or deletion of existing cloud jobs. <br>
Mitigation: Explicitly confirm submit, delete, and other billable or destructive actions before execution. <br>
Risk: Alibaba Cloud credentials and OSS paths may expose sensitive access or media locations if copied into evidence files. <br>
Mitigation: Use least-privilege RAM credentials or roles, avoid storing secrets in evidence, and verify OSS regions and output paths before running jobs. <br>


## Reference(s): <br>
- [IMS video translation parameter reference](references/fields.md) <br>
- [Source list](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-mps-video-translation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and API workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include job parameters, OSS paths, command outputs, and API response summaries for evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
