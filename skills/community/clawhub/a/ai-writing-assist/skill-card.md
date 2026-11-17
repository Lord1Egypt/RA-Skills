## Description:

Helps agents call the Flyelep AI writing API to generate creative copy, improve prompts, and return multiple writing options for image or video creation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request creative product copy, prompt refinements, and inspiration from Flyelep's writing API. The skill also guides agents through collecting required user inputs, handling optional image references, and presenting generated options back to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local image uploads can create permanent unsigned public URLs without a clear consent checkpoint.

Mitigation: Use only non-sensitive prompts and images you are comfortable sending to Flyelep; do not provide confidential product images, personal photos, regulated data, credentials, or private documents unless explicit consent, retention, deletion, and access-control guarantees are available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyelepai/skills/ai-writing-assist)
- [Flyelep API key dashboard](https://www.flyelep.cn/controlboard)
- [Flyelep assisted generation API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/assistedGeneration)
- [Flyelep file upload API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns multiple creative copy options from the API response and may include guidance for request parameters, upload handling, and error recovery.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
