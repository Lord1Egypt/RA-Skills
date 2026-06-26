## Description: <br>
Converts input text to a Chinese female-voice MP3 using edge-tts and installs required Linux tools on first run. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiawhite-sir](https://clawhub.ai/user/iiawhite-sir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users can convert supplied text into an MP3 voice file, especially Chinese narration, from natural-language or command-line skill calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First run can change the Linux environment through sudo apt and pipx installation steps. <br>
Mitigation: Review the script before installing and run it only in an environment where those package changes are acceptable. <br>
Risk: The skill writes to a user-supplied output path and may overwrite an existing file. <br>
Mitigation: Choose a fresh, noncritical MP3 output path and verify the target directory before execution. <br>
Risk: Text-to-speech conversion may use an online service, which can expose submitted text outside the local machine. <br>
Mitigation: Avoid converting sensitive, confidential, or regulated text unless the service behavior and data handling are acceptable. <br>


## Reference(s): <br>
- [ClawHub listing for edge-tts-auto](https://clawhub.ai/iiawhite-sir/edge-tts-auto) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON] <br>
**Output Format:** [MP3 audio file with JSON status response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires text and output_path inputs; writes media to the supplied path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
