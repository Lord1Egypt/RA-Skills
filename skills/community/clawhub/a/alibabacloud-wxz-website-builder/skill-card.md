## Description: <br>
Use when building or modifying websites with AI Staff via Alibaba Cloud OpenAPI, including conversation creation, asynchronous chat, requirement collection, PRD generation, code generation, and incremental SSE event polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and website builders use this skill to create or modify Alibaba Cloud AI Staff website projects, collect requirements, generate PRDs and code, poll build progress, and retrieve preview URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Alibaba Cloud credentials to create website-builder conversations and submit later requirement defaults without asking the user each time. <br>
Mitigation: Install only when this workflow is acceptable, use a least-privilege RAM user instead of root AccessKeys, review generated project data in Alibaba Cloud, and avoid highly sensitive business requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-wxz-website-builder) <br>
- [Alibaba Cloud AccessKey Setup Guide](references/ak-setup-guide.md) <br>
- [AI Staff OpenAPI Overview](references/api_overview.md) <br>
- [RAM Policies - Required Permissions](references/ram-policies.md) <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud AI Website Builder Portal](https://wanwang.aliyun.com/webdesign/home#/ai/manage/prd) <br>
- [Alibaba Cloud RAM Users Console](https://ram.console.aliyun.com/users) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API responses, generated website code, project links, and preview URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Alibaba Cloud credentials resolved through the default credential chain and least-privilege RAM permissions.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
