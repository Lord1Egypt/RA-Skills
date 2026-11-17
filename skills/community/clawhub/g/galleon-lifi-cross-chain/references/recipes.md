# LI.FI API recipes

Checked 2026-09-27. Base URL `https://li.quest/v1`. A public quote can be requested without a wallet signature. API-key requirements and rate limits depend on the integration; use an existing `x-lifi-api-key` secret if required without exposing it.

## Read-only quote

```sh
curl --fail-with-body --silent --show-error --get 'https://li.quest/v1/quote'   --data-urlencode 'fromChain=8453'   --data-urlencode 'toChain=42161'   --data-urlencode "fromToken=$SOURCE_TOKEN"   --data-urlencode "toToken=$DESTINATION_TOKEN"   --data-urlencode 'fromAmount=1000000000'   --data-urlencode "fromAddress=$SENDER"   --data-urlencode "toAddress=$RECIPIENT"   --data-urlencode 'slippage=0.005'
```

The illustrative amount assumes a verified 6-decimal input. Never copy token addresses between chains.

## Read-only status

```sh
curl --fail-with-body --silent --show-error --get 'https://li.quest/v1/status'   --data-urlencode "txHash=$SOURCE_HASH"   --data-urlencode 'fromChain=8453'   --data-urlencode 'toChain=42161'
```

Store source receipt block/hash and status timestamp alongside `sending`, `receiving`, `status`, `substatus`, and `substatusMessage`. The optional returned `quote` helps comparison but does not replace the originally approved terms. Missing quote means retrieve the saved quote or label comparison unavailable.

## Evidence output

`{state, quoteId, sourceHash, sourceReceipt, bridge, destinationHash, recipient, expectedToken, receivedToken, minimumRaw, receivedRaw, gasCosts, refund, nextCheck}`. Unknown values stay unknown. No destination transaction is invented from an estimated duration.

## Primary sources

- [Quote endpoint](https://docs.li.fi/li.fi-api/li.fi-api/requesting-a-quote)
- [Status lifecycle and reconciliation](https://docs.li.fi/introduction/user-flows-and-examples/status-tracking)
- [Quote versus route and step construction](https://docs.li.fi/introduction/user-flows-and-examples/difference-between-quote-and-route)
- [API documentation index](https://docs.li.fi/llms.txt)
- [Official SDK](https://github.com/lifinance/sdk)
- [Contract deployments](https://docs.li.fi/introduction/lifi-architecture/smart-contract-addresses)
