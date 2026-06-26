## Description: <br>
Publishes HTML or Markdown content to Bilibili articles or Tribee posts, handling login checks, title entry, content insertion through the editor API, and publish actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zangzhicong](https://clawhub.ai/user/zangzhicong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to publish prepared HTML or Markdown articles to Bilibili Article or Tribee posts through an authenticated browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish through the user's logged-in Bilibili account without a required final approval step. <br>
Mitigation: Before publishing, verify the account, file path, title, target, visibility, category or sync settings, and require explicit approval before clicking publish. <br>
Risk: Local images referenced by the source HTML or Markdown can be inlined into the content and published. <br>
Mitigation: Review embedded image paths and the processed content before insertion, especially when the source file comes from an untrusted location. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zangzhicong/bili-sunflower-publish) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and browser-action steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces publish workflow instructions and can drive a logged-in browser session to post user-supplied content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
