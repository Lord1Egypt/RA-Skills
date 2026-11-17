## Description:

ClawDaddy helps agents check domain availability, brainstorm available names, get purchase quotes, purchase domains with USDC or cards, and manage DNS and nameservers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gregm711](https://clawhub.ai/user/gregm711)

### License/Terms of Use:


## Use Case:

External users, developers, and AI agents use this skill to find available domain names, compare prices, initiate domain purchases, and manage domain settings after registration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real domain purchases through USDC or card payment flows.

Mitigation: Require explicit user approval after presenting the quote, payment method, total cost, domain name, and registration consequences before any purchase request.

Risk: The skill can change DNS records, nameservers, domain lock state, autorenew settings, and transfer state.

Mitigation: Require explicit approval before DNS deletion, nameserver changes, domain unlocks, autorenew changes, transfer actions, or other administrative changes.

Risk: Management tokens grant control over registered domains and token recovery invalidates previous tokens.

Mitigation: Keep management tokens private, avoid exposing them in shared logs or public responses, and warn users when token recovery will invalidate old tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gregm711/skills/clawdaddy)
- [Publisher profile](https://clawhub.ai/user/gregm711)
- [ClawDaddy](https://clawdaddy.app)
- [ClawDaddy documentation](https://clawdaddy.app/llms.txt)

## Skill Output:

**Output Type(s):** [guidance, API Calls, JSON, text, shell commands, configuration]

**Output Format:** [Markdown guidance with HTTP examples, JSON responses, TXT responses, and bearer-token instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can lead agents through real domain purchase, DNS, nameserver, settings, transfer, and token recovery workflows.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
