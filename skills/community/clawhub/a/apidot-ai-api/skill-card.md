## Description: <br>
Use APIDot as one AI API for image generation API, video generation API, chat API, music generation API, and 3D generation API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan APIDot integrations for image, video, chat, music, and 3D generation workflows, including API-key handling, async task status, polling, and webhook patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real API usage may expose an APIDot API key or send requests to APIDot if the user implements calls from the guidance. <br>
Mitigation: Store APIDOT_API_KEY only in server-side environment variables or a backend secret manager, and avoid placing secrets in chat, browser code, logs, screenshots, or public repositories. <br>
Risk: APIDot model fields, availability, and pricing can change over time. <br>
Mitigation: Check the current APIDot docs and model pages before writing production code or making product commitments. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Models](https://apidot.ai/models) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot Website](https://apidot.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with links and code-oriented integration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference shell commands or API examples from official APIDot documentation, but the artifact itself contains no executable files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
