## Description: <br>
Helps users in China buy McDonald's products with Claw wallet balance and receive a redemption link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vikky-lin](https://clawhub.ai/user/vikky-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users in China use this skill to check Claw wallet balance, view on-sale McDonald's items, and purchase a selected item with an access token before redeeming it in store. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend wallet balance when purchasing products. <br>
Mitigation: Require explicit user confirmation for the item, price, token, and account name before every purchase. <br>
Risk: The access token functions as a payment credential and may expose wallet balance if shared or logged. <br>
Mitigation: Treat the token as sensitive, avoid sharing or logging it, and install only if the Claw wallet provider, API host, and recharge contact are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vikky-lin/buy-mcdonald) <br>
- [Claw Pay API host](https://www.stonetech.top) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, guidance] <br>
**Output Format:** [JSON responses and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return balance details, on-sale product data, payment status, and a McDonald's redemption link.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
