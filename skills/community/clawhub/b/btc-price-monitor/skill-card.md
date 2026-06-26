## Description: <br>
Fetches the current Bitcoin price from CoinGecko and sends it to Telegram, with optional alerts if the price falls below a configured threshold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jesusreb](https://clawhub.ai/user/jesusreb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub users use this skill to check Bitcoin's current USD price and send price updates or threshold alerts to a Telegram chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts CoinGecko and Telegram when run. <br>
Mitigation: Confirm this network behavior before installation and run it only in environments where those outbound requests are expected. <br>
Risk: Telegram notifications use a bot token and chat ID and send messages through a third-party service. <br>
Mitigation: Use a dedicated Telegram bot token, verify the intended chat ID, and avoid placing unrelated secrets or sensitive content in notification messages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jesusreb/btc-price-monitor) <br>
- [CoinGecko simple price API endpoint](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd) <br>
- [Telegram sendMessage API endpoint](https://api.telegram.org/bot<token>/sendMessage) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text Telegram message and console status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID; optional PRICE_THRESHOLD_USD controls threshold alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
