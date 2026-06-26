## Description: <br>
Search 24+ airline loyalty programs for award space with miles cost, seat availability, and jetlag scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travel planners and award-flight agents use this skill to search award-seat availability, compare mileage pricing, calculate cents-per-point value, and manage saved trips or alerts across major airline loyalty programs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Award searches may use travel routes, dates, award-search context, and optional airline loyalty account access. <br>
Mitigation: Confirm the user intends to share that travel context, prefer API searches when possible, and request loyalty credentials only for a specific user-directed lookup. <br>
Risk: Browser-based airline searches can involve logged-in account pages. <br>
Mitigation: Use browser workflows only when needed for visual verification or account-specific searches, confirm before login, and never store or log loyalty credentials. <br>


## Reference(s): <br>
- [Aerobase Awards on ClawHub](https://clawhub.ai/kurosh87/aerobase-awards) <br>
- [Scrapling Documentation](https://scrapling.readthedocs.io/en/latest/overview.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown summaries with API request and response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include award-seat options, mileage prices, seat counts, jetlag scores, fuel-surcharge warnings, cents-per-point calculations, saved trip details, and alert setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
