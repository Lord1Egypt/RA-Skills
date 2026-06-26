## Description: <br>
Gets secure, one-time-use payment credentials, including cards and tokens, from a Link wallet so agents can complete purchases on behalf of users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danhill-stripe](https://clawhub.ai/user/danhill-stripe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and purchasing agents use this skill to authenticate with Link, inspect merchant checkout requirements, create approved spend requests, and retrieve one-time payment credentials for completing purchases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help agents create credentials with real spending power. <br>
Mitigation: Require Link authentication and user approval, and have the user review merchant, item, amount, and shipping details before approving a spend request. <br>
Risk: Card numbers, shared payment tokens, and shipping addresses are sensitive and may leak through transcripts, logs, or temporary files. <br>
Mitigation: Mask sensitive details in conversation, write raw card output only to local files with restricted permissions when needed, and delete temporary credential files after the purchase. <br>
Risk: Suspicious or spoofed checkout pages could misuse issued credentials. <br>
Mitigation: Inspect the merchant page and domain before creating a spend request, avoid suspicious checkout flows, and stop for user verification when page authenticity is uncertain. <br>


## Reference(s): <br>
- [Create Payment Credential on ClawHub](https://clawhub.ai/danhill-stripe/create-payment-credential) <br>
- [Link Agents](https://link.com/agents) <br>
- [Link](https://link.com) <br>
- [MPP Protocol](https://mpp.dev/protocol.md) <br>
- [MPP HTTP 402 Protocol](https://mpp.dev/protocol/http-402.md) <br>
- [MPP Challenges](https://mpp.dev/protocol/challenges.md) <br>
- [Link App](https://app.link.com) <br>
- [Link Support](https://support.link.com/topics/about-link) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to handle sensitive payment credentials, approval URLs, shipping addresses, and temporary local credential files.] <br>

## Skill Version(s): <br>
0.6.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
