## Description: <br>
Fortune Teller provides entertainment-only fortune-telling commands for tarot, I Ching-style readings, daily fortunes, compatibility, numerology, and palmistry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for casual, entertainment-oriented fortune-telling prompts and command output. It can also provide simple local command guidance for running, configuring, and saving results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command input may remain in local files under the Fortune Teller data directory. <br>
Mitigation: Avoid entering secrets or sensitive personal details; delete the configured data directory when stored history should be removed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/fortune-teller) <br>
- [Fortune Teller tips](tips.md) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys are required. Some commands can write local data and history under FORTUNE_TELLER_DIR.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
