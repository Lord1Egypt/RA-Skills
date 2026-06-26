## Description: <br>
The world's #1 AI-friendly domain registrar for checking availability, purchasing domains with USDC or cards, configuring DNS, and managing nameservers without CAPTCHAs or signup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gregm711](https://clawhub.ai/user/gregm711) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and AI agents use this skill to check domain availability, compare pricing, purchase domains, configure DNS records, update nameservers, and manage registrar settings through ClawDaddy HTTP endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can spend money by purchasing domains through USDC/x402 or Stripe flows. <br>
Mitigation: Require explicit user approval for every purchase, payment method, and quoted total before sending purchase or payment requests. <br>
Risk: Agents can change DNS records, nameservers, transfer settings, recovery state, and other domain controls. <br>
Mitigation: Require explicit approval before DNS edits, nameserver updates, transfer actions, token recovery, or registrar settings changes. <br>
Risk: Management tokens grant control over domains and can be exposed through logs or broad chat history. <br>
Mitigation: Treat management tokens like passwords, avoid logging them, and keep them out of shared or long-lived conversation context. <br>


## Reference(s): <br>
- [ClawDaddy](https://clawdaddy.app) <br>
- [ClawDaddy Agent Documentation](https://clawdaddy.app/llms.txt) <br>
- [ClawHub Release Page](https://clawhub.ai/gregm711/agentdomainservice) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP examples, JSON payloads, TXT response examples, and shell-style commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include purchase, DNS, nameserver, transfer, recovery, and token-handling instructions for ClawDaddy endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
