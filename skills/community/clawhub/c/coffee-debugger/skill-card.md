## Description: <br>
Developer coffee decision engine that recommends coffee based on work context, fatigue level, and current time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maximum2974](https://clawhub.ai/user/maximum2974) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill in Claude Code to get concise coffee recommendations for coding, debugging, meetings, documentation, review, incident response, learning, or low-energy work sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad phrases about tiredness, energy, or coffee recommendations. <br>
Mitigation: Review the recommendation before acting on it and invoke the skill intentionally when the conversation is not about coffee or fatigue. <br>
Risk: The skill is allowed to use Bash to check the current time. <br>
Mitigation: Keep shell access constrained to the documented time check behavior, such as `date +%H:%M`, during installation and review. <br>
Risk: Coffee recommendations may be unsuitable for users who are already over-caffeinated or working extreme hours. <br>
Mitigation: Follow the skill's built-in guidance to prefer water, decaf, or sleep-focused advice when users report over-caffeination or sustained exhaustion. <br>


## Reference(s): <br>
- [Coffee Debugger on ClawHub](https://clawhub.ai/maximum2974/coffee-debugger) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown recommendation with diagnosis, prescription, dosage, reasoning, and a developer tip.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use the current time to tailor caffeine guidance.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
