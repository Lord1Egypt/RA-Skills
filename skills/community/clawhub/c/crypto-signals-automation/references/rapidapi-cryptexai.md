# RapidAPI cryptexAI mapping

## Endpoints

### Get symbols

```bash
curl --request GET \
  --url https://cryptexai-buy-sell-signals.p.rapidapi.com/getSymbols \
  --header 'X-RapidAPI-Host: cryptexai-buy-sell-signals.p.rapidapi.com' \
  --header 'X-RapidAPI-Key: <API_KEY>'
```

### Get signals for symbol

```bash
curl --request GET \
  --url 'https://cryptexai-buy-sell-signals.p.rapidapi.com/getSignalsForSymbol?symbol=BCH' \
  --header 'X-RapidAPI-Host: cryptexai-buy-sell-signals.p.rapidapi.com' \
  --header 'X-RapidAPI-Key: <API_KEY>'
```

## Normalization

Input fields used:
- `id` (signal identifier)
- `symbol` (e.g. BCH)
- `action` (BUY/SELL)
- `entry`
- `takeProfits[0..2]`
- `stopLoss`
- `active` (must be true)
- `createdAt`
- `confidence`
- `reason`

Map `symbol` to dYdX market by appending `-USD` where applicable (e.g. `BCH -> BCH-USD`).

## Rate limits

Plan-based monthly quota:
- Pro: 1,000
- Ultra: 10,000
- Mega: 100,000

Implementation guidance:
- Batch symbol pulls in one cycle.
- Use interval scheduling (e.g. 15-30 minutes).
- Cache last processed signal ID per symbol and avoid duplicate processing.
