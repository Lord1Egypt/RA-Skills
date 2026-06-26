## Description: <br>
Automatically selects and uses an AI model for a task based on task type, with optional feedback learning when a user-configured router is enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoyyyceD](https://clawhub.ai/user/JoyyyceD) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to classify substantive tasks and route them to configured model providers for coding, review, reasoning, writing, translation, summarization, data analysis, image understanding, or chat. It can operate locally by selecting from configured providers, or use an explicitly configured self-hosted router for recommendation and feedback learning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation can route ordinary user tasks without the user noticing that model routing is being applied. <br>
Mitigation: Review the skill before installing and use it only when automatic routing is desired for routine prompts. <br>
Risk: Task text may be sent to configured external model providers or to a user-configured router service. <br>
Mitigation: Avoid private, regulated, or secret-bearing tasks unless routing is explicit, provider behavior is understood, and any router endpoint is controlled by the user. <br>
Risk: A router mode can affect which provider receives a task and how feedback is collected. <br>
Mitigation: Confirm the selected provider, what data is sent, and how to disable or limit automatic routing before use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/JoyyyceD/auto-model-router) <br>
- [Publisher profile](https://clawhub.ai/user/JoyyyceD) <br>
- [Project homepage](https://github.com/JoyyyceD/auto-model-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command blocks and concise model-routing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a footer identifying the selected task category and model.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata; artifact frontmatter reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
