# Primary sources and verification

Reviewed 2026-10-02. Current docs and public read behavior are separate evidence.

- [CoinGecko simple price](https://docs.coingecko.com/demo/reference/simple-price): CoinGecko-ID lookup, USD marks and requested `last_updated_at`.
- [CoinGecko Demo daily history](https://docs.coingecko.com/demo/reference/coins-id-market-chart): timestamp/price pairs, daily UTC auto-granularity above 90 days, current Demo range and documented key requirement. The helper probes a distinct unauthenticated public request; a success proves only that bounded public read.
- [CoinGecko methodology](https://www.coingecko.com/en/methodology): aggregate market metrics, not venue execution terms.
- [DefiLlama free endpoint reference](https://api-docs.defillama.com/llms-free.txt): public current price endpoint, timestamp and ID namespaces. The CoinGecko namespace does not make provider agreement independent.
- [DefiLlama official API SDK](https://github.com/DefiLlama/api-sdk): existing provider implementation for broader data workflows; no SDK runtime is copied here.

The helper is an independently authored bounded diagnostic, not a generic adapter service or provider client. Offline tests supply synthetic responses; they exercise IDs, dates, body limits, timeout, redaction, partial failures, aligned comparisons and history gaps without account access or network calls. Research instructions do not establish a running monitor or venue capability.
