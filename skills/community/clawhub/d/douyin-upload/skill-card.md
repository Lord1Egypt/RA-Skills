## Description: <br>
Automatically generates Douyin article content and cover images from a user-provided topic, then publishes them through the sau command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yidahis](https://clawhub.ai/user/yidahis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and social media operators use this skill to draft Douyin articles, create matching cover images, and optionally publish them to a linked Douyin account. Agents can use it for topic-driven article generation, publishing workflow automation, and dry-run content review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish generated content to a live Douyin account by default. <br>
Mitigation: Use --skip-publish or a manual review workflow first, and inspect the generated article and cover image before publishing. <br>
Risk: Generated prompts, article content, responses, and publishing logs may contain sensitive information. <br>
Mitigation: Avoid sensitive prompts, review generated files and logs before sharing, and treat local logs as potentially sensitive. <br>
Risk: The security review reports an unsafe shell command path involving user-influenced filenames. <br>
Mitigation: Use the skill only for intentional Douyin publishing requests and prefer a publisher update that replaces shell execution with argument-list execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yidahis/douyin-upload) <br>
- [references/README.md](references/README.md) <br>
- [references/examples.md](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles, generated image files, JSON logs, and command-line publishing status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write article, image, and log files under the configured workspace and may publish to a linked Douyin account unless publishing is skipped.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
