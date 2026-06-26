## Description: <br>
Handle Clawver customer reviews by monitoring ratings, drafting responses, and tracking sentiment trends for reputation management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwang783](https://clawhub.ai/user/nwang783) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Store operators and support teams use this skill to list Clawver reviews, identify unanswered or negative feedback, draft public responses, monitor sentiment trends, and configure review webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access customer review data, including reviewer contact details shown in API examples. <br>
Mitigation: Use the least-privileged CLAW_API_KEY available and avoid exposing customer emails unless they are needed for support. <br>
Risk: The skill can publish or replace store responses that customers may see. <br>
Mitigation: Review public replies before posting and keep responses professional, accurate, and within the documented length limit. <br>
Risk: Review webhooks can send event data to configured URLs. <br>
Mitigation: Configure webhooks only to URLs you control and use a strong webhook secret. <br>


## Reference(s): <br>
- [Clawver Reviews on ClawHub](https://clawhub.ai/nwang783/clawver-reviews) <br>
- [Clawver](https://clawver.store) <br>
- [Reviews API Examples](references/api-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples, response templates, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW_API_KEY; review responses are capped at 1000 characters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
