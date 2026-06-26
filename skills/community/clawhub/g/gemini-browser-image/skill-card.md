## Description: <br>
Generate images with the user's own Chrome session and Gemini web UI for article covers, illustrations, and social media visuals when the user explicitly asks for image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiao1yin2he3](https://clawhub.ai/user/jiao1yin2he3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to automate image generation through an already-authorized Gemini web session, then download and copy the generated image assets into a target workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a Chrome session that may be logged into Gemini and can observe browser state. <br>
Mitigation: Use a dedicated Chrome profile for Gemini automation, close unrelated tabs, and do not expose cookies, tokens, profile data, or account secrets. <br>
Risk: The skill reads the browser download directory and copies generated files, which can create accidental disclosure or overwrite risk. <br>
Mitigation: Use a non-sensitive download directory and target output folder, then verify the downloaded image before reuse. <br>
Risk: The workflow depends on external browser automation tools. <br>
Mitigation: Verify the mcporter and chrome-devtools-mcp tools before use and run only the commands needed for the current image generation task. <br>


## Reference(s): <br>
- [Gemini web UI](https://gemini.google.com) <br>
- [ClawHub skill page](https://clawhub.ai/jiao1yin2he3/gemini-browser-image) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with PowerShell and mcporter command examples; generated image files are downloaded through the browser.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running Chrome session with remote debugging, an authorized Gemini account, chrome-devtools-mcp access, and a readable download directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
