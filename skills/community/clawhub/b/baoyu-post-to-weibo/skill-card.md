## Description: <br>
Posts content to Weibo, including regular text, image, and video posts and headline articles from Markdown through Chrome CDP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare Weibo posts and long-form Weibo articles from text, media files, or Markdown. It opens Chrome, stages the content in Weibo, and leaves final review and publishing to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses persistent Chrome sessions for Weibo, so it can act in an already-authenticated browser context. <br>
Mitigation: Use a dedicated Chrome profile when possible and review the staged Weibo content before publishing. <br>
Risk: The skill uses the system clipboard and real paste keystrokes while composing articles. <br>
Mitigation: Keep focus on the intended Chrome window during composition and avoid running unrelated clipboard-sensitive workflows at the same time. <br>
Risk: The security scan flagged broad clipboard, keystroke, and Chrome-process control behavior for review. <br>
Mitigation: Install only if that behavior is acceptable for the environment and follow the scanner guidance to review everything carefully before clicking publish. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimliu/baoyu-post-to-weibo) <br>
- [Skill homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-weibo) <br>
- [Weibo](https://weibo.com/) <br>
- [Weibo article editor](https://card.weibo.com/article/v3/editor) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration guidance, Browser automation guidance] <br>
**Output Format:** [Markdown instructions with inline bash commands and browser-staged content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bun or npx, Chrome or Chromium, and a persistent Weibo login session.] <br>

## Skill Version(s): <br>
1.117.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
