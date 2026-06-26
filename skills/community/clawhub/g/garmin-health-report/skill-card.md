## Description: <br>
Generate comprehensive daily health reports from Garmin Connect data with professional running analysis including heart rate zones, TRIMP, and Jack Daniels VDOT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GZZZJ](https://clawhub.ai/user/GZZZJ) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External Garmin Connect users and developers use this skill to authenticate locally, fetch personal Garmin data, and generate daily text health reports with sleep, heart-rate, activity, running-load, and trend analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Garmin login tokens and sessions may remain available after use. <br>
Mitigation: Install only on a trusted machine, inspect ~/.garmin-health-report for oauth1_token.json and oauth2_token.json, and revoke Garmin sessions when needed. <br>
Risk: Local health metrics may be retained after report generation. <br>
Mitigation: Review or delete ~/.garmin_health_report/history.json if local health-history retention is not desired. <br>
Risk: Using the wrong Garmin region can affect authentication behavior. <br>
Mitigation: Confirm whether the account uses garmin.com or garmin.cn before entering Garmin credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GZZZJ/garmin-health-report) <br>
- [Homepage from skill metadata](https://github.com/yourusername/garmin-health-report) <br>
- [garth Garmin Connect library](https://github.com/matin/garth) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text health report with Markdown usage guidance and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+, garth, local Garmin authentication tokens, and optional user age/resting heart rate configuration.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
