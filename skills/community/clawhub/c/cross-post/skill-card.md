## Description: <br>
Cross-post content to Twitter/X, Reddit, and LinkedIn from one prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drspx](https://clawhub.ai/user/drspx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media managers, creators, and developers use this skill to draft, preview, and publish the same post across Twitter/X, Reddit, and LinkedIn through the platforms' APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish externally to social-media accounts using stored credentials and broad posting triggers. <br>
Mitigation: Use preview first, confirm platform destinations before posting, and avoid confidential or unapproved drafts. <br>
Risk: The skill stores social-media API credentials locally. <br>
Mitigation: Keep the config file private, use least-privilege credentials, and rotate tokens if the machine or file is exposed. <br>
Risk: The documented default all-platform command may not publish anywhere until the dispatch issue is fixed. <br>
Mitigation: Specify platforms explicitly or verify script behavior in a controlled account before relying on broad posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drspx/cross-post) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can trigger external social-media posts when posting commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
