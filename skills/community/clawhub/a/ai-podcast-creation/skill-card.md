## Description: <br>
Create AI-powered podcasts with text-to-speech, music, and audio editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and content teams use this skill to generate podcast segments, multi-voice conversations, audiobooks, background music, and merged audio workflows through inference.sh services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Podcast prompts, scripts, and pasted documents may be sent to hosted providers such as inference.sh or OpenRouter. <br>
Mitigation: Avoid secrets, regulated data, and confidential documents unless the user has approval to share that content with the hosted providers. <br>
Risk: The workflow depends on installing and authenticating an external inference.sh CLI. <br>
Mitigation: Install only when the user is comfortable trusting the CLI installer and logging into an inference.sh account; use the published checksum information when verification is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/okaris/ai-podcast-creation) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI installer](https://cli.inference.sh) <br>
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward inference.sh CLI calls that can produce hosted audio outputs through external services.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
