## Description: <br>
Agent S Bridge lets DeepSeek TUI launch Agent-S to control a browser or desktop GUI from natural-language instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangxianzhan](https://clawhub.ai/user/huangxianzhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators can use this skill to check Agent-S setup and launch desktop or browser automation tasks from DeepSeek TUI through shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to enable AI-controlled desktop and browser automation, which can act on files, accounts, forms, and other GUI surfaces. <br>
Mitigation: Use a sandbox, virtual machine, or test browser profile, and manually approve file changes, submissions, purchases, and account actions. <br>
Risk: The skill requires sensitive API credentials for model access. <br>
Mitigation: Use dedicated API keys with limited scope, avoid entering passwords, MFA codes, or payment data during automation, and rotate keys if exposed. <br>
Risk: The security review notes that the wrapper's authority is under-scoped and instruction forwarding is unclear. <br>
Mitigation: Ask the publisher to document safety boundaries and fix instruction forwarding before relying on it for sensitive or unattended workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huangxianzhan/agent-s-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Launches Agent-S locally and may open a new automation window; requires OpenAI or Anthropic API credentials and optional UI grounding endpoint configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
