## Description: <br>
检查并优化中文文章的AI翻译腔，让文本更自然 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terryso](https://clawhub.ai/user/terryso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and technical writers use this skill to review Chinese Markdown articles for AI-translation style and apply targeted edits that make the prose more natural while preserving technical terms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly modify a user-provided Markdown file. <br>
Mitigation: Use it only on files that can be restored from version control or backups, and review the final diff carefully. <br>
Risk: Automated prose edits may change intended wording or nuance. <br>
Mitigation: Ask the agent to show proposed edits before writing when the article is important, and accept only changes that preserve the author's meaning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terryso/de-ai-flavor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown report with inline edit suggestions and a git diff after file modification] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May directly modify the target Markdown file after reporting detected issues.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
