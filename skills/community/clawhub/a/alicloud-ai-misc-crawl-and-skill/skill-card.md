## Description: <br>
Refresh the Model Studio models crawl and regenerate derived summaries and `skills/ai/**` skills when the models list or generated skills must be updated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to crawl Alibaba Cloud Model Studio documentation, rebuild model summaries, and regenerate related local AI skill files and coverage reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow writes generated files and may update `skills/ai/**`, which can create broad workspace changes. <br>
Mitigation: Run it in a branch or disposable workspace and review generated output before committing or publishing. <br>
Risk: The crawl step uses a network package and live Alibaba Cloud documentation, so results can change over time. <br>
Mitigation: Pin or verify the crawler package when repeatability matters and keep crawl artifacts with key parameters for review. <br>


## Reference(s): <br>
- [Alibaba Cloud Model Studio Models](https://help.aliyun.com/zh/model-studio/models) <br>
- [ClawHub Skill Release](https://clawhub.ai/cinience/alicloud-ai-misc-crawl-and-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands plus generated Markdown, JSON, and local skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates crawl summaries, a structured model list, a skill coverage report, and updates under `skills/ai/**`.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
