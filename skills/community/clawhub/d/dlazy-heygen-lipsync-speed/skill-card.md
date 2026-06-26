## Description: <br>
Generate fast lip-sync video by syncing input video and audio using the HeyGen Lipsync Speed model through the dLazy API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to invoke the dLazy CLI for HeyGen Lipsync Speed jobs that align an input video with an audio track and return hosted generation results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be saved locally by the dLazy CLI or supplied through the DLAZY_API_KEY environment variable. <br>
Mitigation: Use an organization-scoped key with the least access available, rotate or revoke it from the dLazy dashboard when needed, and avoid exposing it in prompts, logs, or shared shell history. <br>
Risk: Video and audio files passed to the CLI may be uploaded to dLazy-hosted services for processing. <br>
Mitigation: Review the files for sensitive content before submission and use dry-run or help output to confirm parameters before sending data to the hosted API. <br>
Risk: The artifact documentation has an inconsistency between the listed lip-sync options and a sample prompt-based command. <br>
Mitigation: Run dlazy heygen-lipsync-speed -h and confirm current CLI arguments before executing jobs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlazyai/dlazy-heygen-lipsync-speed) <br>
- [dLazy Homepage](https://dlazy.com) <br>
- [dLazy CLI Repository](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from the dLazy CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return hosted result URLs, or an asynchronous task identifier when no-wait mode is used.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence release version and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
