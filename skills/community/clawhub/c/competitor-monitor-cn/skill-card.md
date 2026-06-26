## Description: <br>
Competitor Monitor tracks competitor product prices, availability changes, and price-change alerts for ecommerce platforms including Taobao, JD, Pinduoduo, and Amazon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt6558609-cpu](https://clawhub.ai/user/zt6558609-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ecommerce sellers and operations teams use this skill to monitor competitor pricing, record local price history, and generate alerts when configured products change price or stock status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured product names, prices, local price history, and price-change alerts may be stored locally or sent to enabled webhooks. <br>
Mitigation: Use trusted HTTPS webhook URLs, keep webhook secrets private, and avoid enabling channels that should not receive monitored product or pricing details. <br>
Risk: Pricing data and generated recommendations may be incomplete, stale, or inaccurate. <br>
Mitigation: Verify important pricing information against the source platform before making business or pricing decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zt6558609-cpu/competitor-monitor-cn) <br>
- [Publisher Profile](https://clawhub.ai/user/zt6558609-cpu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown alerts and reports, JSON configuration, local JSON history files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and uv according to ClawHub metadata; optional webhooks can send configured alert messages.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
