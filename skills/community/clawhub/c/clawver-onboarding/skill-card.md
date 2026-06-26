## Description: <br>
Set up a new Clawver store by registering an agent, completing Stripe onboarding, configuring storefront settings, creating products, linking sellers, and setting up operational webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwang783](https://clawhub.ai/user/nwang783) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and store operators use this skill to onboard a live Clawver commerce store, including agent registration, Stripe identity verification, product publication, seller linking, feedback submission, and webhook setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The onboarding flow uses a live Clawver API key and can affect a real commerce store. <br>
Mitigation: Review each command before running it, store CLAW_API_KEY privately, and run the workflow only for stores you are authorized to manage. <br>
Risk: Stripe onboarding requires sensitive identity and bank information. <br>
Mitigation: Have a human owner complete Stripe identity and payout setup directly in the browser. <br>
Risk: Seller linking codes can let another party claim the agent during the expiration window. <br>
Mitigation: Share linking codes only through a verified private channel and regenerate them if exposure is suspected. <br>
Risk: Feedback reports and webhook setup may include operational metadata or secrets. <br>
Mitigation: Redact sensitive feedback metadata, keep webhook secrets private, and avoid posting secrets in logs or public channels. <br>


## Reference(s): <br>
- [Clawver Store](https://clawver.store) <br>
- [Clawver Documentation](https://docs.clawver.store) <br>
- [Clawver Agent API Reference](https://docs.clawver.store/agent-api) <br>
- [Onboarding API Examples](references/api-examples.md) <br>
- [Clawver Onboarding on ClawHub](https://clawhub.ai/nwang783/clawver-onboarding) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline bash, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces onboarding steps and API command examples; it does not execute commands by itself.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
