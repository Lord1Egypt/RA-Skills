## Description: <br>
Use when users want to subscribe, pay, or manage Crypto Listing Alert notifications for exchange listing events and need Telegram, Discord, or Email delivery with API-key login. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyz-ass](https://clawhub.ai/user/xyz-ass) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manage paid Crypto Listing Alert subscriptions for Binance, OKX, Bybit, and Bitget listing events, including setup, payment orders, status checks, and unsubscribe flows across Telegram, Discord, or Email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Telegram and Discord bot tokens plus API keys, which can expose secrets if copied into logs, shell history, or broad local configuration reads. <br>
Mitigation: Use least-privilege throwaway bots where possible, avoid placing secrets directly on command lines, and only allow access to the exact configuration sources needed for the selected channel. <br>
Risk: Subscription and payment commands can create or continue crypto payment orders. <br>
Mitigation: Confirm plan, exchanges, billing cycle, channel, exact USDT amount, wallet address, and pending-order handling with the user before creating or continuing payment flows. <br>
Risk: Notification delivery can fail when Telegram or Discord bot prerequisites are incomplete. <br>
Mitigation: Verify that the Telegram user has started the configured bot or that the Discord bot is present with send permissions before treating delivery as ready. <br>


## Reference(s): <br>
- [Crypto Listing Alert](https://listingalert.org) <br>
- [Crypto Listing Alert API](https://listingalert.org/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/xyz-ass/crypto-listing-alert) <br>
- [Publisher Profile](https://clawhub.ai/user/xyz-ass) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JSON CLI mode for commands and explicit user-provided or configured credentials for API keys, bot tokens, chat IDs, channel IDs, and email addresses.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
