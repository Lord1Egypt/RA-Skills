## Description: <br>
Repurposes an article into platform-adapted versions for WeChat Official Account, Xiaohongshu, Zhihu, and Douyin while preserving the core ideas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, and marketing teams use this skill to repurpose Markdown or text articles into platform-specific posts and scripts for WeChat Official Account, Xiaohongshu, Zhihu, and Douyin, including preview and batch workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input articles are sent to OpenAI for rewriting. <br>
Mitigation: Use only content approved for external processing; avoid confidential, personal, regulated, or unpublished material unless that data flow is acceptable. <br>
Risk: The skill requires an OpenAI API key and installs Python dependencies. <br>
Mitigation: Use a dedicated API key, protect the local .env file, and install dependencies in a virtual environment. <br>
Risk: AI-generated rewrites can be inaccurate, misleading, or poorly matched to a target platform. <br>
Mitigation: Review generated drafts before publication and edit them for factual accuracy, brand fit, and platform policy compliance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopiabenben/ai-content-tailor) <br>
- [Skill documentation](SKILL.md) <br>
- [Skill metadata](skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Markdown and plain-text article variants, with CLI status messages and optional preview output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write one file per selected platform; batch mode processes Markdown and text inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, SKILL.md frontmatter, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
