## Description: <br>
Security check for ClawHub skills powered by Koi. Query the Clawdex API before installing any skill to verify it's safe. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wearekoi](https://clawhub.ai/user/wearekoi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill before installing ClawHub skills to query Clawdex for a benign, malicious, or unknown verdict. It can also help audit already installed OpenClaw skills and decide when user review is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill checks installed skill names and queries an external Clawdex/Koi security service for verdicts. <br>
Mitigation: Install only when sharing skill names with that external service is acceptable, and avoid including unrelated sensitive context in API requests. <br>
Risk: Clawdex results are advisory and a verdict can be unknown or incomplete. <br>
Mitigation: Review unknown or risky skills before installation and ask for explicit user approval before taking follow-up action. <br>


## Reference(s): <br>
- [Clawdex by Koi on ClawHub](https://clawhub.ai/wearekoi/clawdex) <br>
- [Koi](https://www.koi.ai/) <br>
- [Clawdex skill verdict API](https://clawdex.koi.security/api/skill/SKILL_NAME) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON verdict examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Clawdex API returns advisory verdicts such as benign, malicious, or unknown.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact/SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
