## Description: <br>
Track fridge and pantry inventory with expiry reminders and grocery lists. Use when logging groceries, checking expiry dates, or building shopping lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use Fridge to log fridge and pantry inventory, review recent household entries, export records, and build grocery or maintenance lists from a local command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Household notes are saved locally in plaintext-like files under ~/.local/share/fridge/. <br>
Mitigation: Avoid entering sensitive personal details on shared or heavily backed-up machines, and review local file permissions before use. <br>
Risk: The skill text describes expiry reminders, but evidence warns not to rely on it for real timed expiry alerts without verification. <br>
Mitigation: Use a separate trusted reminder system for time-critical expiry or safety decisions. <br>


## Reference(s): <br>
- [Fridge on ClawHub](https://clawhub.ai/bytesagain-lab/fridge) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and shell command output, with export files available as JSON, CSV, or text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user-entered inventory notes locally under ~/.local/share/fridge/.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
