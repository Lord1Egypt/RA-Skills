## Description: <br>
ClawHealth Data Skill lets an agent query the hosted ClawHealth service for authorized HealthKit data, nutrition records, goals, readiness signals, reports, anomaly context, and temporary visual panels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hengruizzzz](https://clawhub.ai/user/hengruizzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their personal agents use this skill to connect authorized ClawHealth data to daily or weekly health summaries, readiness and nutrition questions, mood logging, and temporary visual panels. It is for wellness context and does not provide diagnosis, treatment, or emergency guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill works with sensitive health, nutrition, mood, readiness, and profile data through a hosted service. <br>
Mitigation: Install only when the user intends the agent to use ClawHealth, send only authorized data to clawhealth.site, and keep the Agent API token out of chats, logs, and repositories. <br>
Risk: A long-lived Agent API token can continue granting access if it is exposed. <br>
Mitigation: Treat the token like a password and delete or rotate it in the ClawHealth iOS app when access should stop. <br>
Risk: Health and readiness outputs could be mistaken for medical or performance diagnosis. <br>
Mitigation: Present results as wellness context from the latest synced data, separate data from interpretation, and avoid diagnosis, treatment, or emergency guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hengruizzzz/clawhealth-data-skill) <br>
- [ClawHealth service site](https://clawhealth.site) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with HTTPS API request guidance and temporary panel links when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses authorized ClawHealth data and tokens supplied by the user; panel links are temporary.] <br>

## Skill Version(s): <br>
0.5.1 (source: server evidence release.version and artifact README publish command) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
