## Description: <br>
Runs bazi chart generation, dayun analysis, full-report generation, and chat context building for user-facing astrology questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gycdsj](https://clawhub.ai/user/gycdsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to generate Chinese bazi astrology reports and answer astrology questions from birth date, birth time, gender, and a user prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birth date/time, gender, and user questions may be sent to a configured OpenClaw/OpenAI-compatible model provider. <br>
Mitigation: Use only with trusted model configuration, avoid collecting unnecessary personal details, and tell users what information is sent for analysis. <br>
Risk: The auxiliary convert.py script contains an unsafe shell command path. <br>
Mitigation: Do not invoke convert.py in production; remove it or replace the shell command with a safe argument-list subprocess call before direct CLI use. <br>
Risk: Astrology output can be mistaken for factual professional advice. <br>
Mitigation: Present responses as cultural or entertainment-oriented guidance and avoid using them as the sole basis for medical, legal, financial, or safety decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gycdsj/bazi-astrology) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Chinese text or Markdown report with a bazi detail table and analysis sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires birth date/time and gender for full reports; may request missing birth information before analysis.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
