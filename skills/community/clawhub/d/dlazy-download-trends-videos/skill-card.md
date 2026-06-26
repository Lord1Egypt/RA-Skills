## Description: <br>
Downloads a single YouTube video from a trends URL and returns a hosted video file URL with metadata such as title, duration, and resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download a selected YouTube trends video through the dLazy CLI and receive a hosted video URL with title, duration, and resolution metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and sends video URLs and task parameters to dLazy services. <br>
Mitigation: Install and run it only when the user trusts dLazy with those inputs; store the API key through the documented CLI flow and rotate or revoke it from the dashboard if exposed. <br>
Risk: The skill returns hosted output URLs and may process private, regulated, or copyrighted video content. <br>
Mitigation: Use it only for content the user has rights to process and avoid private or regulated material unless appropriate controls are in place. <br>
Risk: A global CLI install persists an executable on the user's system. <br>
Mitigation: Use the pinned npx invocation when a persistent global install is not desired, and review the dLazy CLI source before installation when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-download-trends-videos) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with CLI examples; command execution returns JSON from the dLazy CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The command result includes a hosted video file URL and video metadata; asynchronous runs may return a generation ID for polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
