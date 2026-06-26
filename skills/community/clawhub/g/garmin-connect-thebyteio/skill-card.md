## Description: <br>
Integrates with Garmin Connect to fetch and analyze sleep, body battery, resting heart rate, stress, and training status for recovery-aware training summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vegasbrianc](https://clawhub.ai/user/vegasbrianc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and personal fitness agents use this skill to authenticate to Garmin Connect, fetch daily wellness metrics, and produce recovery-aware training summaries or nudges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Garmin credentials and local session tokens are sensitive. <br>
Mitigation: Use a dedicated Garmin 1Password item, restrict the 1Password token to the needed vault and item, and secure or delete /tmp/garmin-session on shared systems. <br>
Risk: Dependency setup and bundled scripts execute locally and may affect the user's Python environment. <br>
Mitigation: Install dependencies in a virtual environment and review the shell scripts before running them. <br>
Risk: Fetched health metrics may be cached in local files. <br>
Mitigation: Use a private GARMIN_CACHE_DIR location and delete cached metrics when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vegasbrianc/garmin-connect-thebyteio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON metric output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use 1Password-backed Garmin credentials, local Garmin session tokens, and optional local health-metric cache files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
