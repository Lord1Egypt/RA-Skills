# 🔐 Agent Pay Client

Explicit-consent-only client for x402 (USDC) and L402 (Lightning) HTTP 402
paywalls. Works with any compliant server — not tied to one platform.

## Why "explicit-consent-only"

AI agents transacting autonomously is a real and growing pattern (x402
alone has processed 150M+ transactions). It's also a real risk if done
carelessly: an agent that pays based on page content or hidden
instructions, with no spending limit, is a liability. This library's
rule: **no credentials configured, no spending ceiling set → no payment,
ever** — regardless of what a paywalled resource asks for.

## Install

```bash
pip install -r requirements.txt
```

## Usage

```python
from agent_pay_client import AgentPayClient, PayerConfig

# Look before you pay
client = AgentPayClient()
print(client.get_payment_options("https://api.example.com/paid"))

# Pay for real, with an explicit ceiling
config = PayerConfig(evm_private_key="0x...", max_x402_atomic="50000")
result = AgentPayClient(config).fetch("https://api.example.com/paid")
```

## Supported protocols

- **x402** — USDC/EVM stablecoin payments over HTTP (Coinbase/Cloudflare,
  Linux Foundation x402 Foundation)
- **L402** — Lightning Network payments (manual-approval by default;
  auto-pay requires explicit LND credentials)

## License

MIT

## Support

Free and open source. If it saved you time, voluntary support is welcome:

- Website: https://btc-vision.org
- BTC: `bc1qtpuhwl0vnhrch5p7e5469q2ed66hlyyvh8rtsn`
- ETH: `0xf03b429d4d85896a46dd7a64b5a8ab9f0bbb4ced`
- SOL: `3G5UZHFYN8hbv3aTZt6Lr7qqx4FTTkAyLJq34HjQLraz`
- Lightning: `welove@blink.sv`
