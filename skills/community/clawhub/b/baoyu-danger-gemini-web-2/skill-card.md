## Description: <br>
Generates images and text through a reverse-engineered Gemini Web API, with support for prompt-based text generation, image generation, reference-image vision input, and multi-turn conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nengnengZ](https://clawhub.ai/user/nengnengZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill when they need a local CLI backend for Gemini Web text generation, image generation, reference-image vision input, or continuation of saved Gemini conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse a browser-authenticated Google/Gemini session and store live cookies on disk. <br>
Mitigation: Use a dedicated Chrome profile or GEMINI_WEB_CHROME_PROFILE_DIR, consider a dedicated Google account, and protect or periodically delete the cookie file. <br>
Risk: Reference images and prompt files can be sent to Gemini Web during generation. <br>
Mitigation: Review local files before passing them as prompt or reference inputs, and avoid sensitive files unless upload is intended. <br>
Risk: The skill relies on a reverse-engineered Gemini Web client. <br>
Mitigation: Install and run it only when that dependency model is acceptable for the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nengnengZ/baoyu-danger-gemini-web-2) <br>
- [Metadata homepage](https://github.com/JimLiu/baoyu-skills#baoyu-danger-gemini-web) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Plain text or JSON on stdout, with optional generated image files saved to disk.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can maintain saved conversation sessions and can read prompt files or reference images as inputs.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
