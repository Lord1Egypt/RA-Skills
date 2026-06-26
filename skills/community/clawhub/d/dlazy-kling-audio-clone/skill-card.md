## Description: <br>
Generate customized speech that highly restores the timbre by uploading reference audio using Kling Audio Clone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to invoke the dLazy CLI for Kling Audio Clone voice-cloning tasks with a reference audio URL or local audio file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload voice data and generate cloned speech without clear consent safeguards. <br>
Mitigation: Use only voices and audio that the user has clear rights and consent to use, and verify the local audio file before upload. <br>
Risk: The artifact documentation contains mismatched media workflow details and command examples. <br>
Mitigation: Review command help before execution and do not rely on the documented examples until the publisher fixes the output schema and examples. <br>
Risk: The skill requires a sensitive dLazy API key. <br>
Mitigation: Prefer per-use environment variables or the documented CLI auth flow, rotate or revoke keys when needed, and avoid exposing credentials in prompts or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-kling-audio-clone) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key and may upload the selected reference audio file to dLazy-hosted services.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
