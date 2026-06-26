## Description: <br>
Posts text, images, videos, quote posts, and long-form articles to X/Twitter through a logged-in Chrome browser session, with optional public submission automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[praguepp](https://clawhub.ai/user/praguepp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and marketing teams use this skill to prepare X/Twitter posts, media posts, quote posts, and X Articles from agent workflows. It is intended for logged-in browser publishing where the user reviews composed content before posting, unless the user explicitly enables automated submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate a logged-in X/Twitter account and publish public content when submission is enabled. <br>
Mitigation: Use preview workflows by default and enable submission only after reviewing the exact post, article, media, and target account. <br>
Risk: Browser automation uses an authenticated Chrome profile, which can expose the user's active session to unintended actions. <br>
Mitigation: Use a dedicated Chrome profile for this skill and avoid sharing the profile with normal browsing sessions. <br>
Risk: Fallback workflows can overwrite or depend on the desktop clipboard and real keystrokes. <br>
Mitigation: Warn users before clipboard-based operations, keep Chrome as the intended foreground target, and verify the composed content after paste operations. <br>
Risk: Markdown articles may include remote images that the workflow downloads before inserting into X Articles. <br>
Mitigation: Use trusted markdown inputs only and review remote image URLs before running article publishing workflows. <br>
Risk: Automatic Chrome process cleanup can terminate browser automation sessions unexpectedly. <br>
Mitigation: Do not allow automatic Chrome process killing unless the user has reviewed what will be terminated. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/praguepp/baoyu-post-to-x-enhanced) <br>
- [Homepage Listed In ClawHub Metadata](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-x) <br>
- [Regular Posts Reference](artifact/references/regular-posts.md) <br>
- [X Articles Reference](artifact/references/articles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May compose or publish content through a local authenticated browser session; preview mode is the default for documented workflows unless submission is explicitly requested.] <br>

## Skill Version(s): <br>
3.0.0 (source: SKILL.md frontmatter, ClawHub release evidence, README version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
