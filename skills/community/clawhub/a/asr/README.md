# Speech is Cheap: ClawHub ASR

Give your agent audio or video from a URL or local file and get a transcript
from [Speech is Cheap](https://speechischeap.com/). Results can be JSON, SRT,
or VTT, with optional speaker labels, word timestamps, and sound labels.
Asynchronous jobs support webhook delivery and status retrieval.

The skill supports Speech is Cheap API keys and wallet payments through x402.
Wallet mode pays per job in USDC on Base from your existing wallet, up to a
price ceiling you approve, with no Speech is Cheap account.

## Install

OpenClaw:

```sh
openclaw skills install asr
```

Hermes Agent:

```sh
hermes skills install clawhub/asr
```

Other agents that use the ClawHub CLI (installs into `./skills/asr` under the
current folder):

```sh
clawhub install asr
```

API-key mode requires Bash, curl, and a Speech is Cheap account. Configure
`SIC_API_KEY` in your agent's environment, or set `skills.entries.asr.apiKey`
in OpenClaw's config.

Wallet mode needs Node.js 22 or newer, pnpm, and an existing EVM wallet
holding USDC on Base. Install its dependencies with
`pnpm install --frozen-lockfile` from the installed skill directory.

[SKILL.md](SKILL.md) tells your agent how to transcribe, recover a purchase,
retrieve results, and cancel a paid job.
See the [source repository](https://github.com/speechischeap/clawhub-asr)
for maintenance guidance.
