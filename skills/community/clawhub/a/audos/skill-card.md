## Description: <br>
Audos helps agents create AI-powered startup workspaces with landing pages, brand identity, workspace tools, and an AI assistant through the Audos API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[werdelin](https://clawhub.ai/user/werdelin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and their agents use this skill to turn a startup idea into an Audos workspace with a landing page, brand identity, business tools, and Otto assistant access. It is most relevant when a user wants to start a business, build an MVP, validate an idea, or launch a product workflow through Audos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived Audos auth tokens may grant continued account access if retained insecurely. <br>
Mitigation: Store Audos tokens only in a secure credential store with explicit user consent, and provide clear revocation and deletion paths. <br>
Risk: Workspace creation and later actions involving outreach, ads, payments, or customer data can affect real users and business operations. <br>
Mitigation: Use only emails the user controls, avoid confidential business or customer data unless the user trusts Audos, and require explicit confirmation before those actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/werdelin/audos) <br>
- [Audos agent onboarding API](https://audos.com/api/agent/onboard) <br>
- [Audos website](https://audos.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and API request and response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes polling updates, workspace URLs, and Audos API status responses when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
