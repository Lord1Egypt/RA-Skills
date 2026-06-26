## Description: <br>
Orchestrates an AI-assisted WeChat Official Account content pipeline that routes topic planning, drafting, review, formatting, image generation, and publishing through the companion WeChat article skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiworkskills](https://clawhub.ai/user/aiworkskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, editors, and brand content teams use this skill to run a WeChat Official Account article from topic selection through draft, review, layout, images, and draft or publication handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires WeChat and model-provider credentials. <br>
Mitigation: Keep aws.env out of version control, restrict repository access, and use least-privilege credentials where possible. <br>
Risk: Publishing behavior can send content to WeChat when the companion publishing subskill is configured. <br>
Mitigation: Review the publishing subskill before enabling posting, and keep publish_method set to draft unless external publication is explicitly intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiworkskills/aws-wechat-article-main) <br>
- [AIWorkSkills homepage](https://aiworkskills.cn) <br>
- [First-time setup](references/first-time-setup.md) <br>
- [Configuration example](references/config.example.yaml) <br>
- [Environment variable example](references/env.example.yaml) <br>
- [Article screening schema](references/articlescreening-schema.md) <br>
- [Writing specification example](references/writing-spec.example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Full workflow use requires configured aws.env and .aws-article/config.yaml files plus companion WeChat article subskills.] <br>

## Skill Version(s): <br>
1.0.25 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
