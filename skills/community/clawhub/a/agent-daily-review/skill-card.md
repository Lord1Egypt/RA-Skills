## Description: <br>
Helps agents conduct structured end-of-day review, reflection, documentation, activity categorization, and Markdown report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use this skill to review a day's workspace notes and artifacts, categorize work, identify highlights and blockers, and create an archived daily review report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local workspace notes, daily memory files, MEMORY.md, and Markdown artifacts while building the review. <br>
Mitigation: Run it only against the intended workspace path and avoid workspaces containing notes that should not be summarized. <br>
Risk: The default run writes a review report and appends a summary to MEMORY.md. <br>
Mitigation: Use --no-memory when the review should not modify MEMORY.md, and set --output to a known destination when testing. <br>
Risk: The documented cron setup can repeatedly trigger local reads and writes without a manual prompt. <br>
Mitigation: Enable scheduled runs only after verifying the workspace path, output behavior, and retention expectations. <br>


## Reference(s): <br>
- [Agent Daily Review on ClawHub](https://clawhub.ai/openlark/agent-daily-review) <br>
- [Core review script](artifact/scripts/daily_review.py) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown report with structured review sections and optional memory summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reviews/review_YYYY-MM-DD.md and can append a summary to MEMORY.md unless --no-memory is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
