## Description: <br>
Flowsery helps agents query Flowsery Analytics for website traffic, visitor behavior, revenue, conversion data, and confirmed goal or payment record management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tarasshyn](https://clawhub.ai/user/tarasshyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Flowsery-tracked site performance, summarize real-time and historical analytics, review revenue and conversion trends, and manage goal or payment records when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Flowsery API key that can access analytics, revenue, visitor profile PII, and payment data. <br>
Mitigation: Install only when the publisher is trusted, use the narrowest available token, and never expose the token in output, logs, or client-side code. <br>
Risk: Visitor profiles and payment records can include personal data such as email, name, location, revenue, and activity history. <br>
Mitigation: Retrieve personal data only for explicit, authorized requests and present the minimum detail needed to answer the user. <br>
Risk: Goal and payment delete operations are irreversible and can erase historical business data. <br>
Mitigation: Restate the website, filters, date range, and affected records when known, then require explicit user confirmation before any delete request. <br>
Risk: Goal or payment writes can add personal or business records. <br>
Mitigation: Send only fields needed for the task and avoid optional personal fields unless the user explicitly provides them for attribution. <br>


## Reference(s): <br>
- [ClawHub Flowsery Skill Page](https://clawhub.ai/tarasshyn/flowsery) <br>
- [Flowsery Homepage](https://flowsery.com) <br>
- [Flowsery Analytics API Reference](references/api-reference.md) <br>
- [Breakdown Dimensions Reference](references/breakdown-dimensions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with curl command examples and summarized API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FLOWSERY_API_KEY and may access analytics, revenue, visitor profile PII, payment data, and confirmed write or delete operations.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
