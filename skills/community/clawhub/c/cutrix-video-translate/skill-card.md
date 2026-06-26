## Description: <br>
Guides agents to use the Cutrix Python SDK for video translation, dubbing, subtitles, and voice-clone workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wallacerao](https://clawhub.ai/user/wallacerao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate Python guidance, code examples, install commands, and polling patterns for submitting Cutrix video translation tasks with an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos, audio, subtitles, and task metadata may be sent to Cutrix for cloud processing. <br>
Mitigation: Use the skill only for media approved for Cutrix processing, and avoid confidential or regulated media unless explicitly authorized. <br>
Risk: API keys can be exposed if they are hard-coded or passed through visible command lines. <br>
Mitigation: Use the CUTRIX_API_KEY environment variable and avoid embedding credentials in generated code, repositories, or command invocations. <br>
Risk: Hot-loop polling can create unnecessary request volume while Cutrix tasks process asynchronously. <br>
Mitigation: Poll task status with a delay and stop when the task reaches a success or failure terminal state. <br>


## Reference(s): <br>
- [Cutrix](https://www.cutrix.cc) <br>
- [Cutrix Video Translate on ClawHub](https://clawhub.ai/wallacerao/cutrix-video-translate) <br>
- [Publisher profile](https://clawhub.ai/user/wallacerao) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference CUTRIX_API_KEY and Cutrix task IDs; generated examples should avoid hard-coded secrets.] <br>

## Skill Version(s): <br>
v1.1.4 (source: evidence release metadata; artifact frontmatter says 1.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
