## Description: <br>
Get the physical location of your macOS device and print it to stdout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerrykfc](https://clawhub.ai/user/jerrykfc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to retrieve the device's current physical location with CoreLocationCLI, including one-shot, watch, formatted text, and JSON output modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The command prints current physical location, which is sensitive personal data. <br>
Mitigation: Run it only when the current session may see the Mac's location, and avoid including results in shared logs, screenshots, or transcripts. <br>
Risk: Watch mode can continuously expose updated location values. <br>
Mitigation: Use --watch only when continuous updates are needed, and stop the command when the task is complete. <br>
Risk: Installation depends on a Homebrew cask and macOS Gatekeeper approval. <br>
Mitigation: Verify the Homebrew cask or upstream project before installing, and approve the app only through macOS Privacy & Security when expected. <br>


## Reference(s): <br>
- [CoreLocationCLI on ClawHub](https://clawhub.ai/jerrykfc/corelocationcli) <br>
- [jerrykfc publisher profile](https://clawhub.ai/user/jerrykfc) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash command examples and plain text or JSON CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Swift, Location Services approval, and Wi-Fi for reliable location lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
