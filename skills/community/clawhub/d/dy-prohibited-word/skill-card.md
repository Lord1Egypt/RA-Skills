## Description: <br>
检测文案、文件或网页中的抖音违禁词并加粗显示，提供违禁词替换建议和仅替换违禁词后的文案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, e-commerce operators, live-stream script planners, and marketing teams use this skill to check Douyin copy, uploaded text files, extracted image text, or webpage text for prohibited words before publication. It returns highlighted risks, replacement suggestions, and a revised copy file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checked text and extracted webpage or file content is sent to RedFox for processing. <br>
Mitigation: Use the skill only for content appropriate to send to RedFox over HTTPS, and avoid highly sensitive internal documents. <br>
Risk: The skill requires a RedFox API key. <br>
Mitigation: Use a scoped, revocable key and do not hard-code or expose it in prompts, logs, code, or output files. <br>
Risk: The skill writes revised copy to a local text file. <br>
Mitigation: Delete generated output files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/dy-prohibited-word) <br>
- [Core workflow](references/core_workflow.md) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox service](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown sections with tables and bold highlights, plus a generated plain-text revised-copy file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; checks content in batches when input exceeds 3000 characters and stops above 10000 characters.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
