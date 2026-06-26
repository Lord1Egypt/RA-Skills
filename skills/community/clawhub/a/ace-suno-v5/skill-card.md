## Description: <br>
Suno V5 Music provides a local browser interface and Python client for generating music through the AceData Suno API, with support for simple and custom creation modes and local saving of audio, cover art, and lyrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyunnet](https://clawhub.ai/user/xiyunnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a local web app or Python client that submits prompts, lyrics, styles, and advanced generation options to AceData's Suno API and saves generated music files locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill automatically installs unpinned Python packages. <br>
Mitigation: Review before installing, run in an isolated virtual environment, and pin dependencies before regular use. <br>
Risk: The security scan reports that the AceData API key is stored in browser localStorage. <br>
Mitigation: Use a dedicated low-scope API key, avoid confidential prompts or lyrics, and clear browser localStorage and history after use. <br>
Risk: The security scan reports under-scoped local server controls in the web app. <br>
Mitigation: Run the app only on localhost in a trusted environment and review server behavior before exposing it beyond the local machine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiyunnet/ace-suno-v5) <br>
- [AceData Suno API endpoint](https://api.acedata.cloud/suno) <br>
- [AceData API key signup](https://share.acedata.cloud/r/1uN88BrUTQ) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, Python code examples, shell commands, and locally generated music files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated assets are saved under the user's Desktop music directory by date when the local app runs successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
