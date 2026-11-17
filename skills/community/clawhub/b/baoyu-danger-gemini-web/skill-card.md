## Description: <br>
Generates images and text via reverse-engineered Gemini Web API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate Gemini Web text responses, image files, JSON responses, and multi-turn conversation outputs from prompts and optional reference images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is an unofficial Gemini Web client that can reuse a Google browser session and cache live session cookies locally. <br>
Mitigation: Use a dedicated Chrome profile or custom data directory, avoid reusing normal browsing sessions, and delete stored cookies and session files when finished. <br>
Risk: Prompts and reference files may be sent to Gemini Web during text, vision, or image generation. <br>
Mitigation: Avoid sending sensitive local files, private prompts, secrets, or regulated data unless the user has explicitly approved that use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimliu/baoyu-danger-gemini-web) <br>
- [Project homepage from ClawHub metadata](https://github.com/JimLiu/baoyu-skills#baoyu-danger-gemini-web) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, JSON] <br>
**Output Format:** [Plain text, JSON, saved image files, or saved image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can preserve multi-turn session state in local session files when a session ID is used.] <br>

## Skill Version(s): <br>
1.56.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
