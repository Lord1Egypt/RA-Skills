## Description: <br>
Generates AI videos through the Baiyin open platform, including text-to-video, image-to-video, and task status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuping520](https://clawhub.ai/user/jiuping520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure Baiyin video generation jobs, collect required prompt and media inputs, submit tasks, and poll for generated video results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Baiyin API key for authenticated requests to a third-party video service. <br>
Mitigation: Use a scoped Baiyin API key, store it in the environment, and rotate or revoke it if exposed. <br>
Risk: Local media paths may be uploaded automatically to Baiyin when a URL is not supplied. <br>
Mitigation: Provide only media intended for upload and avoid sensitive files or signed URLs. <br>
Risk: The security evidence flags hidden remote update checks and automatic media uploads for review. <br>
Mitigation: Review before installing and require update checks and uploads to be explicit in deployment policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiuping520/baiyin-video-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jiuping520) <br>
- [API schema reference](references/api-schema.md) <br>
- [Error and polling reference](references/error-and-polling.md) <br>
- [Interaction rules](references/interaction-rules.md) <br>
- [Example flow](references/example-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request/response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BAIYIN_API_KEY, may upload local media to Baiyin, submits generation tasks, and polls task status until completion, failure, or timeout.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
