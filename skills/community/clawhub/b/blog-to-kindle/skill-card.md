## Description: <br>
Scrape blogs and essay sites, compile the collected writing into a Kindle-friendly EPUB with cover art, and optionally send the result to a Kindle address. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ainekomacx](https://clawhub.ai/user/ainekomacx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to fetch supported blogs or custom essay archives, compile posts into EPUB files, and prepare Kindle delivery. It is intended for personal document conversion workflows that require review before any email is sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can email generated files through the user's Mail app and includes a built-in personal Kindle address. <br>
Mitigation: Remove the built-in Kindle email address, require the recipient address to be supplied explicitly, and confirm the exact file and destination before sending. <br>
Risk: Automated Kindle delivery sends attachments from the user's email account. <br>
Mitigation: Use local fetching and EPUB generation first, and enable Mail.app or AppleScript delivery only after reviewing the output and approving the send action. <br>


## Reference(s): <br>
- [Manual Blog-to-Kindle Workflow](references/manual-workflow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ainekomacx/blog-to-kindle) <br>
- [Paul Graham Essays](https://paulgraham.com/articles.html) <br>
- [Kevin Kelly: The Technium](https://kk.org/thetechnium/) <br>
- [Derek Sivers Blog](https://sive.rs/blog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated markdown, EPUB, cover image, manifest, and state files when scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local web fetching, pandoc, cover generation through a separate image skill, and Mail.app delivery on macOS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
