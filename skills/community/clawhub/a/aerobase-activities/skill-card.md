## Description: <br>
Discover Viator tours, attractions, and activities near airports with ratings, reviews, and booking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External travelers and trip-planning agents use this skill to discover airport-area tours, attractions, layover activities, and recovery-friendly options. It helps compare activity duration, ratings, reviews, prices, and connection feasibility before suggesting off-airport plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use travel APIs and occasional browser or Scrapling lookups that share trip-planning details with external services. <br>
Mitigation: Ask the agent to confirm before browsing or using supplemental lookups when travel details should stay private. <br>
Risk: The skill depends on AEROBASE_API_KEY for primary API access. <br>
Mitigation: Use a scoped, revocable API key and rotate it if exposed. <br>
Risk: Activity suggestions can be unsafe if connection time, transit, or delay risk is not checked. <br>
Mitigation: Use the layover feasibility checks and keep the documented 90-minute buffer before suggesting off-airport activities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kurosh87/aerobase-activities) <br>
- [Scrapling documentation](https://scrapling.readthedocs.io/en/latest/overview.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown recommendations with activity details and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include price_from_usd, viator_rating, viator_review_count, duration_minutes, and viator_booking_url when activity results are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
