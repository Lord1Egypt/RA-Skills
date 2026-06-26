## Description: <br>
Blogger API CLI for managing blog posts, including publishing, editing, deleting, listing, searching, scheduling, and monitoring Blogger blogs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saiteja007-mv](https://clawhub.ai/user/saiteja007-mv) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and content operators use this skill to manage Google Blogger posts from an assistant or command line. It supports OAuth setup, post creation, editing, deletion, listing, monitoring, and bulk publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, update, or delete Blogger content using Google OAuth authority. <br>
Mitigation: Use draft mode and explicit per-post review before publishing or changing posts; protect the OAuth token and revoke it when finished. <br>
Risk: Bulk publishing, update, and generation scripts can change many public posts or local content files, including TechRex-specific paths outside the normal Blogger workflow. <br>
Mitigation: Prefer scripts/gblog.py for normal Blogger work; run bulk, update, or generate scripts only after reviewing target blog ID, paths, generated HTML, and exact posts to change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/saiteja007-mv/gblog) <br>
- [Blogger API v3 documentation](https://developers.google.com/blogger/docs/3.0/reference) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate authenticated Blogger API actions when the user runs the provided commands with OAuth credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
