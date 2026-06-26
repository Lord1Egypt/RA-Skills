## Description: <br>
Uses 1Password CLI credentials to sign in to a target website with a headless browser, then completes requested authenticated tasks such as screenshots, page extraction, or downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals or teams use this skill when they want an agent to retrieve a selected 1Password item, log in to the item's website, and complete a bounded post-login task such as capturing a screenshot, extracting page content, or downloading a file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to 1Password credentials and authenticated website sessions. <br>
Mitigation: Use a narrowly scoped 1Password service account, confirm the exact vault, item, site, and task before each run, and never print or write passwords. <br>
Risk: Post-login tasks may expose private account data or create sensitive downloads. <br>
Mitigation: Avoid financial or destructive account actions, keep each task bounded, and delete sensitive files saved in ./downloads when finished. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/1password-browser-login) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with shell commands, browser action guidance, and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save screenshots or downloads under ./downloads and reference them with MEDIA paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
