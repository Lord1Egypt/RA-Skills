## Description: <br>
Generate fixed-template daily AI news posters from five news items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoyacheng](https://clawhub.ai/user/caoyacheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, editors, and agent users use this skill to turn exactly five AI news items into a concise Chinese or bilingual social poster with source and tag metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled manual includes an rm -rf reinstall command that can delete files if the path is changed or expanded incorrectly. <br>
Mitigation: Verify the expanded path is exactly ~/.openclaw/skills/ai-news-poster and back up the existing directory before running the reinstall command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caoyacheng/ai-news-poster) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/caoyacheng) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [PNG poster image with optional normalized JSON and concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires exactly five news items; the local renderer uses Pillow and writes a 1080x1350 PNG.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
