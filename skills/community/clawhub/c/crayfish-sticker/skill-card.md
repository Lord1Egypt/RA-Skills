## Description: <br>
Crayfish Sticker helps an assistant select and send context-aware stickers from a remotely hosted sticker index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StudyWorkLife](https://clawhub.ai/user/StudyWorkLife) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and conversational agents use this skill to add sticker responses based on conversation mood, keywords, and scenarios. It is intended for chat enrichment rather than task automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically add sticker responses based on conversation context. <br>
Mitigation: Lower the sendFrequency setting or avoid installing the skill when automatic sticker responses are not desired. <br>
Risk: The sticker index is retrieved from a GitHub URL that can change over time. <br>
Mitigation: Review the configured repoUrl and the fetched sticker index before deployment in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/StudyWorkLife/crayfish-sticker) <br>
- [Remote Sticker Index](https://raw.githubusercontent.com/StudyWorkLife/crayfish-stickers/main/index.json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, configuration] <br>
**Output Format:** [Markdown text with image links or sticker responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May retrieve and cache a remote sticker index; default send frequency is documented as 0.3.] <br>

## Skill Version(s): <br>
0.1.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
