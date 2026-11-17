---
name: blackwood-state
description: "Use when an agent needs live onchain data (token prices on Base, wallet balances and portfolio value on Ethereum, Base and Solana, ENS names, gas fees, new token pools), ECB exchange rates, or quick AI text utilities (summarize, translate, sentiment). Each call costs US$0.003 to US$0.05 in USDC on Base over x402, paid from the agent's own AgentCash or Coinbase Agentic Wallet after the user approves."
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
    envVars:
      - name: BLACKWOOD_CREDITS_KEY
        required: false
        description: Optional prepaid credit key (bwk_...) for the Blackwood MCP server. Not needed with AgentCash or the Agentic Wallet.
      - name: BLACKWOOD_PRIVATE_KEY
        required: false
        description: Optional, advanced mode of the Blackwood MCP server only. A dedicated Base wallet key the server signs payments with. Not needed with AgentCash or the Agentic Wallet.
    homepage: https://github.com/Blackwood-State/mcp
---

# Blackwood State pay-per-call APIs

33 HTTP endpoints for agents, most of them first-party: onchain reads straight from the chain, ECB reference rates and Workers AI text tools. No account and no API key. Each endpoint answers HTTP 402 with its price, and the agent pays that one call in USDC on Base over x402 with the wallet it already has.

## Cost and approval

- Every call below is paid, from US$0.003 to US$0.05. The table shows the list price; what counts is the price in the 402 answer, which can be lower during a price test.
- **Ask the user before the first paid call** and agree on a budget. Do not pay more than the price in the 402: the commands below cap each payment with `--max-amount`.
- A call that fails, or that the endpoint rejects as bad input (HTTP 400), is not charged.
- This skill is free. It only tells the agent how to call and pay; it holds no key and runs nothing by itself.

## How to call

First, optional and free: `GET` on any endpoint returns its input schema and a real output example.

**AgentCash** (it creates its own wallet on first use; the wallet needs USDC on Base):

```bash
npx -y agentcash@0.17.1 fetch '<endpoint>' -m POST -b '<json body>' --max-amount <price in USD, e.g. 0.005>
```

**Coinbase Agentic Wallet** (the user signs in once with `npx -y awal@2.12.2 auth login <email>`):

```bash
npx -y awal@2.12.2 x402 pay '<endpoint>' -X POST -d '<json body>' --max-amount <price in USDC atomic units, 1000000 = US$1>
```

**MCP** (the same endpoints as tools, with a free demo credit for the first calls):

```bash
claude mcp add blackwood -- npx -y @blackwood-state/mcp@0.2.0
```

Routes marked "(job)" answer `{ jobId, pollUrl }`: GET `pollUrl` (free) until `done` is true and read `output`. Every paid answer carries `next`, the paid call that usually continues the task.

## Endpoints

### Find, read and condense: news, web pages, PDFs and audio into short text

| Task | Endpoint | Price | Example JSON body |
|---|---|---|---|
| News headlines search | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/news-headlines` | US$0.008 | `{"query":"climate finance","limit":3}` |
| Crypto news | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/crypto-news` | US$0.005 | `{"hours":24,"limit":5}` |
| Web page to Markdown | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/web-markdown` | US$0.01 | `{"url":"https://httpbin.org/html","maxChars":500}` |
| PDF to text (job) | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/pdf-text` | up to US$0.05 | `{"url":"https://pdfobject.com/pdf/sample.pdf"}` |
| Speech to text (job) | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/speech-to-text` | up to US$0.05 | `{"url":"https://upload.wikimedia.org/wikipedia/commons/b/bb/Neil_Armstrong_small_step.wav"}` |
| Summarize text | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/summarize` | US$0.008 | GET the route for the schema and an example |
| Translate text | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/translate` | US$0.012 | `{"text":"Pay only for the requests you make.","from":"en","to":"pt"}` |
| Sentiment analysis | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/sentiment` | US$0.004 | `{"texts":["The checkout was fast and the support team was great.","The package arrived broken and nobody answered my emails."]}` |
| LLM chat completion (job) | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/llm-chat` | up to US$0.03 | `{"messages":[{"role":"user","content":"In one sentence, what is the x402 payment protocol?"}],"maxTokens":80}` |
| News research briefing | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/news-briefing` | US$0.04 | `{"topic":"bitcoin","hours":24}` |
| Company research dossier | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/company-dossier` | US$0.03 | `{"domain":"apple.com","ticker":"AAPL","name":"Apple"}` |

### Domain, website and endpoint checks

| Task | Endpoint | Price | Example JSON body |
|---|---|---|---|
| Domain intelligence | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/domain-intel` | US$0.02 | `{"domain":"example.com","certificates":false}` |
| Security headers | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/http-headers` | US$0.007 | `{"url":"https://example.com"}` |
| x402 endpoint check | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/x402-check` | US$0.007 | `{"url":"https://x402.org/protected"}` |
| Email validation | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/email-check` | US$0.005 | `{"email":"postmaster@ietf.org"}` |
| Email list check | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/email-batch` | US$0.02 | `{"emails":["postmaster@ietf.org","test@mailinator.com","info@example.com","not-an-email"]}` |

### FX rates, FX history and company financials

| Task | Endpoint | Price | Example JSON body |
|---|---|---|---|
| Currency exchange rates | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/fx-rates` | US$0.005 | `{"base":"USD","symbols":["EUR","BRL","JPY","GBP"],"amount":100}` |
| Historical exchange rates | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/fx-history` | US$0.005 | `{"symbols":["USD","BRL"],"days":7}` |
| SEC company financials | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/sec-facts` | US$0.02 | `{"ticker":"AAPL"}` |

### Token prices, wallet balances, ENS names and gas fees on Ethereum, Base and Solana

| Task | Endpoint | Price | Example JSON body |
|---|---|---|---|
| Token price on Base | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/token-price` | US$0.003 | `{"token":"WETH"}` |
| Wallet balances on Base | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/wallet-balances` | US$0.004 | `{"address":"0x5A6c77758820182484EA8DE614FC65423E80749a"}` |
| ENS name lookup | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/ens-lookup` | US$0.005 | `{"name":"vitalik.eth"}` |
| Gas price and fees | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/gas-fees` | US$0.003 | `{}` |
| Wallet portfolio and history | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/wallet-portfolio` | US$0.005 | `{"address":"0xFf918CFB0690FdEd4224DBDab916F6E6F78882b7","chains":["base"],"historyLimit":2}` |
| Wallet value in USD | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/wallet-value` | US$0.005 | `{"address":"0x87DB3C25d1E8E40f8EF240D48a711B0C355CF8Cf","chains":["base"]}` |
| Altcoin discovery on Base | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/altcoin-discovery` | US$0.005 | `{"hours":24,"limit":3}` |

### Weather, airport delays and time zones

| Task | Endpoint | Price | Example JSON body |
|---|---|---|---|
| Weather forecast | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/weather-forecast` | US$0.003 | `{"latitude":59.9139,"longitude":10.7522,"hours":3}` |
| Airport delays | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/airport-delays` | US$0.007 | `{}` |
| Time zones | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/timezone` | US$0.003 | `{"time":"2026-11-03T09:00","from":"America/New_York","to":["Europe/London","Asia/Tokyo","America/Sao_Paulo"]}` |

### Images, speech and QR codes

| Task | Endpoint | Price | Example JSON body |
|---|---|---|---|
| Image generation (job) | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/image-gen` | US$0.03 | `{"prompt":"A brass lighthouse on a dark navy sea at dusk, minimalist flat illustration","steps":4}` |
| Text to speech | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/text-to-speech` | US$0.023 | `{"text":"Hello from Blackwood State. This audio was generated on demand.","lang":"en"}` |
| QR code | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/qr-code` | US$0.004 | `{"text":"https://x402-gateway.blackwoodstate8.workers.dev","ecc":"M"}` |

### Random numbers and hashing

| Task | Endpoint | Price | Example JSON body |
|---|---|---|---|
| Random numbers | `POST https://x402-gateway.blackwoodstate8.workers.dev/v1/random` | US$0.005 | `{"kind":"dice","count":2,"sides":6}` |

OpenAPI with every schema: https://x402-gateway.blackwoodstate8.workers.dev/openapi.json. Availability over 30 days: https://x402-gateway.blackwoodstate8.workers.dev/status.json.
