## Description: <br>
Posts text, media, quote posts, and Markdown-based articles to X through a real Chrome session using the selected browser-control workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and agent users use this skill to prepare regular X posts, quote posts, video posts, and long-form X Articles from text, media, or Markdown. It guides browser-controlled composition while requiring review before public submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a real Chrome/X session and prepare externally visible posts. <br>
Mitigation: Verify the active browser profile, target X account, draft content, and media before approving any Post or Publish action. <br>
Risk: Clipboard writes and paste keystrokes can affect the wrong destination if browser focus is incorrect. <br>
Mitigation: Confirm Chrome focus and the intended editor field before pasting, and avoid running the workflow while sensitive clipboard contents are active. <br>
Risk: Automatic Chrome CDP cleanup guidance can terminate browser processes unexpectedly. <br>
Mitigation: Confirm process cleanup with the user before terminating Chrome or Chromium sessions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jimliu/baoyu-post-to-x) <br>
- [Source Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-x) <br>
- [Regular Posts Reference](references/regular-posts.md) <br>
- [X Articles Reference](references/articles.md) <br>
- [Codex Chrome Extension File Upload Documentation](https://developers.openai.com/codex/app/chrome-extension#upload-files) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and browser workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare content in a real Chrome/X session; final public posting requires explicit user confirmation.] <br>

## Skill Version(s): <br>
1.58.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
