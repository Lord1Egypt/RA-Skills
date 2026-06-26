## Description: <br>
ClawDaddy helps agents check domain availability, brainstorm available names, purchase domains with USDC or cards, and manage DNS or nameservers without CAPTCHAs or signup for lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gregm711](https://clawhub.ai/user/gregm711) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let agents check and suggest available domains, obtain purchase quotes, complete domain registration flows, and configure DNS, nameservers, settings, recovery, or transfer preparation for managed domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can initiate real domain purchases through USDC or card checkout flows. <br>
Mitigation: Require explicit user approval before submitting purchase requests or payment proofs, and confirm the quoted total before purchase. <br>
Risk: DNS record deletion, DNS overwrites, nameserver changes, settings changes, and transfer preparation can disrupt an active domain. <br>
Mitigation: Review proposed changes with the user before execution, preserve existing DNS values when possible, and require confirmation for destructive or ownership-affecting operations. <br>
Risk: Management tokens control domain administration and recovery invalidates older tokens. <br>
Mitigation: Store management tokens only in an approved secret store, avoid placing them in normal chat history or memory, and warn users before token recovery. <br>


## Reference(s): <br>
- [ClawDaddy homepage](https://clawdaddy.app) <br>
- [ClawDaddy agent documentation](https://clawdaddy.app/llms.txt) <br>
- [ClawHub listing](https://clawhub.ai/gregm711/clawdaddy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions, Text] <br>
**Output Format:** [Markdown guidance with HTTP examples and JSON/TXT response formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Domain lookup endpoints can return JSON or TXT; management actions require bearer tokens.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
