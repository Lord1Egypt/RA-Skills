## Description: <br>
Posts Weibo text, media, and Markdown-based headline articles by composing content in a logged-in Chrome or Chromium session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nengnengZ](https://clawhub.ai/user/nengnengZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to prepare Weibo posts and long-form articles from text, media files, or Markdown, then review and publish them manually in Weibo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate a real logged-in Chrome or Chromium session for Weibo. <br>
Mitigation: Use a dedicated Chrome profile and review composed content before publishing. <br>
Risk: Clipboard automation can expose or overwrite sensitive clipboard contents. <br>
Mitigation: Avoid sensitive clipboard contents while it runs and clear unrelated secrets before use. <br>
Risk: Its documented troubleshooting path may kill Chrome or Chromium debugging processes automatically. <br>
Mitigation: Run it in an isolated browser profile or session and avoid active browser debugging work during execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nengnengZ/baoyu-post-to-weibo-2) <br>
- [Baoyu Post to Weibo Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-weibo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bun or npx, Chrome or Chromium, and a logged-in Weibo session; scripts compose content for manual review rather than publishing automatically.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
