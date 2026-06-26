## Description: <br>
Generates text and images through a reverse-engineered Gemini Web flow with support for prompt files, reference images, JSON output, and multi-turn sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate Gemini Web text or image outputs, analyze reference images, and preserve conversation context when a Google/Gemini web session is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a reverse-engineered Gemini Web flow and depends on Google/Gemini browser session state. <br>
Mitigation: Use it only when that access model is acceptable, and prefer a dedicated Chrome profile and private data directory. <br>
Risk: Google cookies and saved sessions may persist locally after use. <br>
Mitigation: Avoid high-value Google accounts, limit sensitive prompts or reference files, and periodically delete saved cookies and session files when they are no longer needed. <br>


## Reference(s): <br>
- [Baoyu Danger Gemini Web homepage](https://github.com/JimLiu/baoyu-skills#baoyu-danger-gemini-web) <br>
- [ClawHub skill page](https://clawhub.ai/jimliu/baoyu-danger-gemini-web) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Guidance] <br>
**Output Format:** [Plain text, JSON, generated image files, and saved session records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Bun or npx, a browser-based Google/Gemini session, and local cookie/session storage.] <br>

## Skill Version(s): <br>
1.56.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
