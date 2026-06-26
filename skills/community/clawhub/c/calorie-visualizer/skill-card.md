## Description: <br>
Local calorie logging and visual reporting (auto-refreshes and returns report image after each log). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VintLin](https://clawhub.ai/user/VintLin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill to log meals, estimate calorie and protein intake, and generate refreshed visual nutrition reports from local records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal history and optional photo paths are stored in a local SQLite database. <br>
Mitigation: Install only in workspaces where local health and food logs are acceptable, and limit access to the generated database and report files. <br>
Risk: Food search terms may be sent to USDA when the optional online fallback is enabled. <br>
Mitigation: Use --offline or leave USDA_API_KEY unset when food search terms should remain local. <br>
Risk: Profile-derived calorie targets can use personal health fields from USER.md. <br>
Mitigation: Set config.daily_goal manually or set config.user_refused_profile True when profile-based target calculation is not desired. <br>
Risk: Report rendering depends on Python packages and a local Chromium or Chrome runtime. <br>
Mitigation: Keep the Python dependencies and browser runtime patched before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/VintLin/calorie-visualizer) <br>
- [README](README.md) <br>
- [Quick Start](QUICK_START.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [CLI text, summaries, and REPORT_IMAGE paths to generated PNG reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates a local SQLite database and daily report image.] <br>

## Skill Version(s): <br>
1.0.0 (source: CHANGELOG, package.json, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
