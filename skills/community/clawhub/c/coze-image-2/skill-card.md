## Description: <br>
Coze Image helps an agent generate images from text prompts by running a configurable Coze Seedream 4.5 workflow through the Coze API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rookiebug1216](https://clawhub.ai/user/rookiebug1216) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn image prompts into Coze-hosted image URLs, with an optional local download path when they need a saved file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to Coze through an external API. <br>
Mitigation: Install and use the skill only when sending prompts to Coze is acceptable for the intended data. <br>
Risk: The Coze API token is configured in the script and could be exposed if the configured file is shared or committed. <br>
Mitigation: Store the token outside committed source when possible and avoid sharing configured copies of the script. <br>
Risk: The optional save mode downloads remote image content to a local path. <br>
Mitigation: Use the -o option only with an explicit safe output path. <br>


## Reference(s): <br>
- [Coze homepage](https://www.coze.cn) <br>
- [Coze workflow API endpoint](https://api.coze.cn/v1/workflow/run) <br>
- [ClawHub skill page](https://clawhub.ai/rookiebug1216/coze-image-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown instructions and JSON command results containing image URLs and optional local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Coze image URLs in the form https://s.coze.cn/t/xxx/ and may write an image file when an explicit output path is supplied.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
