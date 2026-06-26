## Description: <br>
X/Twitter CLI for reading, searching, posting, and engagement via cookies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qwarranto](https://clawhub.ai/user/qwarranto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent invoke the bird CLI for X/Twitter reading, search, timelines, account inspection, engagement, posting, and media uploads through cookie-based authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access an X/Twitter account through browser cookies or directly supplied session cookies. <br>
Mitigation: Use a dedicated browser profile or test account where possible, and avoid passing session cookies directly on the command line. <br>
Risk: The skill can post, reply, upload media, follow, unfollow, and otherwise change public account state. <br>
Mitigation: Require manual approval before any posting, media upload, follow, unfollow, or other account-changing action. <br>


## Reference(s): <br>
- [Bird homepage](https://bird.fast) <br>
- [ClawHub skill page](https://clawhub.ai/qwarranto/bird-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional CLI JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local bird CLI and X/Twitter authentication cookies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
