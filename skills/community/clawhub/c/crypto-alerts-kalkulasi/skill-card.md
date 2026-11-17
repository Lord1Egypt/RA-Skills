## Description:

Kelola alert trade-setup crypto top-50: tambah/lihat/hapus setup, jawab konfirmasi pasang/SL+, dan proses alert berkala. Gunakan saat user menulis perintah setup (alert BTC long entry ... tp ... cl ...), menjawab 'pasang', 'sudah <harga>', 'batal', 'ga jadi', atau meminta status alert crypto.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junkevin88](https://clawhub.ai/user/junkevin88)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to track crypto trade setups for top-50 cryptocurrencies and receive chat alerts for entry, stop-loss-plus, take-profit, and cut-loss thresholds. Users confirm and manage setups manually; the skill does not place exchange orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags account login and skill publishing activity beyond the stated crypto-alert purpose, while the required permissions and command scope remain unexplained.

Mitigation: Review the skill's permissions and command scope, and avoid installation until the publisher explains this activity.

Risk: The security review reports an alert-price issue, and its review was incomplete.

Mitigation: Independently verify market prices before acting on alerts; use them as informational prompts rather than financial advice or exchange orders.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/junkevin88/skills/crypto-alerts-kalkulasi)
- [CoinGecko market data API](https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1)
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price?ids=&vs_currencies=usd)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text chat alerts and setup-management guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts are generated from user-defined setup thresholds; no exchange orders are executed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
