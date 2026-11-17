## Description:

TokenBroker routes AI API calls through a local gateway that manages model selection, budget checks, and usage cost statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenrl2006](https://clawhub.ai/user/wenrl2006)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route LLM calls through TokenBroker, monitor broker health, review API usage statistics, and coordinate routing with TokenBudget budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may run npm install in an external token-broker project and execute that project's server code.

Mitigation: Audit the external TokenBroker project and its dependencies before installation or run the service manually from a trusted checkout.

Risk: The installer may append a persistent token-broker program to ~/supervisord.conf.

Mitigation: Review Supervisor changes before use and remove or disable the token-broker entry if persistent startup is not desired.

Risk: LLM calls are routed through a broker that records usage and cost statistics.

Mitigation: Use the skill only where routing through TokenBroker and retaining usage records matches the user's privacy and operational expectations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wenrl2006/skills/ai-token-broker)
- [Publisher Profile](https://clawhub.ai/user/wenrl2006)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown with command-oriented guidance and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start or configure a local TokenBroker service on localhost:8766 when installed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
