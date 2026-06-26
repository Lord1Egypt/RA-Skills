## Description: <br>
Formats terminal commands and their complete outputs into clear, step-by-step Markdown, including errors, long output, interactive prompts, background tasks, and short interpretations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical agents use this skill to present terminal work transparently, showing each command, stdout, stderr, exit details, and a concise interpretation for setup, troubleshooting, and operational workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Displayed command output can reveal secrets, personal data, private paths, hostnames, or service details. <br>
Mitigation: Redact tokens, passwords, API keys, cookies, private infrastructure details, and personal data before sharing or publishing output. <br>
Risk: Example command transcripts may include mutating operations that could be copied into a live environment. <br>
Mitigation: Confirm explicit user intent and review the target environment before running mutating commands shown in examples or generated walkthroughs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pikaqiuyaya/command-output-display) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with fenced shell and output blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include summarized long output, error interpretation, and prompts for user action when commands require interaction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
