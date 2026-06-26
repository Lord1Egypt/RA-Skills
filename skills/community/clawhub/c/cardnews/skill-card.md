## Description: <br>
Generate Instagram-ready card news image sets from a topic, including slide planning, image-generation prompts, PNG to JPG conversion, caption writing, and Instagram upload preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, marketers, and agent users can use this skill to turn a topic into a five-slide Instagram carousel workflow with Korean card-news copy, visual prompts, JPG conversion commands, and caption guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide publication to Instagram using a logged-in browser session. <br>
Mitigation: Review every slide, caption, hashtag, and target account before approving any upload. <br>
Risk: The conversion script may install Pillow from Python package indexes at runtime if it is missing. <br>
Mitigation: Install and review dependencies in a controlled environment before running the conversion step. <br>


## Reference(s): <br>
- [Cardnews design guide](references/design-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with slide plans, image prompts, bash commands, captions, and generated JPG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces five 1:1 carousel slide assets and Instagram upload preparation guidance when used end to end.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
