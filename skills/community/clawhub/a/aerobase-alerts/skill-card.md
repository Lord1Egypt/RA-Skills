## Description: <br>
Real-time flight operations center for delays, cancellations, and gate changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External travelers and travel operations agents use this skill to monitor upcoming flights, contextualize delays, cancellations, gate changes, boarding, and connection risk, and prepare recovery options when disruption occurs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate high-impact travel actions such as rebooking flights. <br>
Mitigation: Require explicit user confirmation before any rebooking, including itinerary, traveler, total cash or miles cost, fees, refund rules, and account to charge. <br>
Risk: The skill stores recent flight-number and alert timestamp history in a local file. <br>
Mitigation: Tell the user where alert history is stored, keep only the minimum needed for deduplication, and prune entries older than seven days. <br>
Risk: The skill may require calendar or booking-account access to assess conflicts and recovery options. <br>
Mitigation: Use least-privilege account access and ask for user consent before reading or acting on calendar or booking data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API Calls, JSON] <br>
**Output Format:** [Markdown or plain text responses with API request actions and local JSON alert-history updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain a local alert-history JSON file for notification deduplication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
