## Description: <br>
Formats Markdown articles into WeChat-compatible HTML with inline styling, selectable themes, font-size and color options, and local preset support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiworkskills](https://clawhub.ai/user/aiworkskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content editors, independent authors, and article production teams use this skill to convert Markdown drafts into WeChat-ready HTML. It helps agents choose or apply formatting themes, run the local formatter, and produce article.html for review before pasting into the WeChat editor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python formatting script with filesystem access to article folders and preset directories. <br>
Mitigation: Run it only on intended article folders and review the generated article.html before pasting it into WeChat. <br>
Risk: Custom theme files in the shared home preset directory can change generated article styling. <br>
Mitigation: Keep ~/.aws-article/presets/formatting content trusted, or remove that directory if shared custom themes are not needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aiworkskills/aws-wechat-article-formatting) <br>
- [Publisher Profile](https://clawhub.ai/user/aiworkskills) <br>
- [Project Homepage](https://aiworkskills.cn) <br>
- [Preset Theme Reference](references/presets/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and a generated WeChat-compatible HTML file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with python3, reads article and preset files, and writes article.html for user review.] <br>

## Skill Version(s): <br>
1.0.24 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
