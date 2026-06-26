## Description: <br>
Provides a local command-line placeholder for Coze Studio-style agent development tasks, including help, status, simple data logging, search, and export commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents can use this skill to run a small local shell utility for status checks, simple data entry, search, and export workflows. Security evidence indicates it should be treated as a placeholder utility rather than the full Coze Studio platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is materially over-described and appears to be a local placeholder utility rather than the full Coze Studio platform. <br>
Mitigation: Review the bundled scripts before installation and do not rely on this skill for full Coze Studio functionality. <br>
Risk: Commands can write local data and history files under the configured data directory. <br>
Mitigation: Set COZE_STUDIO_DIR to a controlled location and review or clear that directory after use. <br>
Risk: Arguments may be written to local logs or data files. <br>
Mitigation: Avoid passing secrets, tokens, private data, or sensitive prompts as command arguments. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bytesagain-lab/coze-studio) <br>
- [Publisher homepage](https://bytesagain.com) <br>
- [Referenced upstream Coze Studio project](https://github.com/coze-dev/coze-studio) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text command output with shell usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read local files under COZE_STUDIO_DIR, defaulting to the user's local data directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
