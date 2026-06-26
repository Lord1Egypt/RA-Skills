## Description: <br>
Book flights, hotels, and eSIMs on cryptotraveler.com with Bitcoin and other cryptocurrencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[g33kme](https://clawhub.ai/user/g33kme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel agents use this skill to search flights, hotels/stays, and eSIM packages, create booking orders, and continue to hosted checkout with cryptocurrency payment support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Linked account access may expose account details and booking history when user-specific endpoints are used. <br>
Mitigation: Use account and booking-history endpoints only for explicit user requests and avoid sharing unnecessary itinerary, identity, or payment-related details. <br>
Risk: Agent credentials and user access tokens can authorize travel actions and account lookups. <br>
Mitigation: Send credentials only to agents.cryptotraveler.com, redact secrets in user-visible output, and revoke or regenerate any exposed secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/g33kme/crypto-traveler) <br>
- [CryptoTraveler homepage](https://www.cryptotraveler.com) <br>
- [CryptoTraveler agent API base](https://agents.cryptotraveler.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON, HTTP, Python, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON or compact TOON API responses where supported; protected endpoints require signed requests.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
