## Description: <br>
Cremonix provides delayed BTC/ETH regime classifications and constraint-filtered setup signals from its production ML trading ensemble. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cremonix](https://clawhub.ai/user/cremonix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading analysts use this skill to fetch Cremonix's delayed BTC/ETH JSON feed and summarize current regimes, setup status, and paid real-time access options for informational market context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a paid upgrade flow that can create subscriptions, request Lightning payment, handle API keys, and renew service. <br>
Mitigation: Use the free delayed feed by default, and require explicit user confirmation plus verification of amount, destination, and billing terms before any subscription, payment, API-key use, or renewal. <br>
Risk: The feed and setup status could be mistaken for financial advice. <br>
Mitigation: Present results as informational market context only, and avoid telling users whether to trade, sit out, or commit funds. <br>
Risk: The free feed includes promotional upgrade messaging. <br>
Mitigation: Disclose the 4-hour delay and paid nature of real-time access, and use the feed only where promotional messaging is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cremonix/cremonix-signals) <br>
- [Cremonix website](https://cremonix.com) <br>
- [Cremonix public delayed feed](https://blog.cremonix.com/feeds/cremonix-free.json) <br>
- [Cremonix OpenClaw docs](https://docs.cremonix.com/openclaw) <br>
- [Cremonix real-time subscription](https://app.cremonix.com/api-subscribe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with optional JSON snippets and curl/jq commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a delayed public JSON feed by default; paid real-time access can involve subscriptions, payments, and API keys.] <br>

## Skill Version(s): <br>
1.2.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
