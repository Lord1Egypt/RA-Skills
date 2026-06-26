## Description: <br>
Posts image-text notes to Xiaohongshu via Chrome CDP, with support for multiple images, title and description entry, topics, and optional auto-submit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[praguepp](https://clawhub.ai/user/praguepp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and publish image-text notes to Xiaohongshu through a logged-in Chrome session, normally leaving the post for user review unless --submit is supplied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a logged-in Xiaohongshu account. <br>
Mitigation: Use a dedicated Chrome profile and review prepared posts in the browser before publishing. <br>
Risk: The --submit option can publish automatically. <br>
Mitigation: Avoid --submit unless automatic posting is intended. <br>
Risk: Chrome debugging session management can affect other browser automation. <br>
Mitigation: Avoid automatic Chrome process killing when other automation may be running. <br>
Risk: Probe or debug scripts may print private account or draft content to logs. <br>
Mitigation: Avoid probe and debug scripts in shared terminals or CI logs, and sanitize logs before sharing. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/praguepp/baoyu-skills#baoyu-post-to-xhs) <br>
- [Xiaohongshu creator publishing page](https://creator.xiaohongshu.com/publish/publish) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can drive a Chrome browser session to preview or submit a Xiaohongshu post depending on user-selected parameters.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
