## Description: <br>
Teach the two-layer CLI architecture enabling AI agents to run shell commands natively with lossless execution and adaptive LLM presentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design shell-centered agents that preserve raw command execution while presenting binary data, long output, stderr, and exit metadata in a form an LLM can use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell-command focused agents can execute destructive, networked, or sensitive-file operations if deployed without controls. <br>
Mitigation: Use sandboxing or least-privilege accounts, add approval gates for destructive or networked commands, and avoid running against sensitive files unless necessary. <br>
Risk: Temporary files created for full command output may retain private data. <br>
Mitigation: Clean up temporary output files after inspection and avoid storing sensitive command output longer than needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1477009639zw-blip/cli-agent-architecture) <br>
- [SKILL.md](SKILL.md) <br>
- [binary_guard.py](scripts/binary_guard.py) <br>
- [truncator.py](scripts/truncator.py) <br>
- [stderr_capture.py](scripts/stderr_capture.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python helper scripts and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local helper scripts for binary detection, output truncation, and stderr formatting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
