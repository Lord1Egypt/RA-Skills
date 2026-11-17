## Description:

Discover Viator tours, attractions, and activities near airports with ratings, reviews, and booking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:


## Use Case:

External travelers and travel-planning agents use this skill to find tours, attractions, and layover activities near airports, including connection feasibility, recovery-stage suggestions, and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations may include affiliate booking URLs and prioritize Aerobase results.

Mitigation: Disclose affiliate booking links to users and compare against neutral sources when the user asks for unbiased recommendations.

Risk: The skill may call Aerobase endpoints and limited browser or Scrapling requests to third-party travel sites.

Mitigation: Only query destinations or activities the user requested, and avoid sending unnecessary personal or itinerary-sensitive details.

Risk: Layover feasibility can change with flight delays, transit time, airport procedures, or minimum connection-time rules.

Mitigation: Check current flight status, connection requirements, and transit time before suggesting off-airport activities.

Risk: Over-broad searches can exceed intended API usage patterns.

Mitigation: Follow the documented search limit of 30 attraction or tour searches per hour and avoid pre-fetching all cities.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kurosh87/skills/aerobase-activities)
- [Scrapling Documentation](https://scrapling.readthedocs.io/en/latest/overview.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown or concise text with activity names, prices, ratings, durations, feasibility notes, and booking URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Viator affiliate booking URLs and Aerobase API result fields.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
