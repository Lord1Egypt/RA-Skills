## Description: <br>
AI-powered content creation workflow for slides, documents, diagrams, websites, data visualizations, research reports, storybooks, financial analysis, images, and related Anygen task outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supertilico2001](https://clawhub.ai/user/supertilico2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run an Anygen CLI workflow that discovers supported operations, gathers requirements, creates content generation tasks, waits for results, and delivers or iterates on generated files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Feishu/Lark delivery path reads local app secrets and sends files through raw API calls. <br>
Mitigation: Use least-privilege Feishu/Lark app credentials, verify the destination chat before sending, and avoid uploading confidential files unless Anygen and the messaging destination are approved for that data. <br>
Risk: The workflow requires sensitive Anygen credentials and trust in the installed @anygen/cli package. <br>
Mitigation: Install only if Anygen and @anygen/cli are trusted, scope credentials to the minimum needed access, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/supertilico2001/anygen-workflow-generate) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/supertilico2001) <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu image upload API endpoint](https://open.feishu.cn/open-apis/im/v1/images) <br>
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Files] <br>
**Output Format:** [Markdown with inline shell commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, download, preview, and deliver generated files; requires the anygen CLI and ANYGEN_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
