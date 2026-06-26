## Description: <br>
Uses optimized prompts to screen batches of football matches and produce single-match win/draw/loss predictions with confidence scores, CLV estimates, and risk factors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingvergil](https://clawhub.ai/user/kingvergil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to rank daily football fixtures for prediction quality and to analyze individual matches for outcome, confidence, CLV, and risk signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends match feature text to DeepSeek or a configured DeepSeek-compatible endpoint, which may expose private or proprietary notes. <br>
Mitigation: Use a dedicated API key, verify DEEPSEEK_BASE_URL before running, and exclude private or proprietary material from input files. <br>
Risk: The skill requires a DEEPSEEK_API_KEY credential. <br>
Mitigation: Store the key in environment variables or a secret manager, rotate it as needed, and do not commit it in files or logs. <br>
Risk: Predictions and CLV estimates may be inaccurate or misleading for betting or other financial decisions. <br>
Mitigation: Review predictions independently and do not rely on the skill as the sole basis for wagering or financial decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kingvergil/football-prediction-optimized) <br>
- [Publisher profile](https://clawhub.ai/user/kingvergil) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON prediction and screening results, with text guidance when invoked through an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stage1 returns ranked match screening results; Stage2 returns a single-match prediction, confidence, CLV estimates, risk factors, and timestamp.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
