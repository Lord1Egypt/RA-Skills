# Recalls by YMM

Model-line safety recalls by year, make, and model. No VIN required.

```
GET https://api.carsxe.com/v1/recalls-ymm?key=$CARSXE_KEY&year={YEAR}&make={MAKE}&model={MODEL}&source=openclaw
```

## Parameters

| Name | Required | Notes |
| --- | --- | --- |
| `year` | yes | 4-digit model year, 1900 through current model year plus one |
| `make` | yes | Manufacturer (case-insensitive) |
| `model` | yes | Model name (case-insensitive) |

## Present

- `data.recall_count` and `data.has_recalls`
- For each recall: NHTSA campaign number, manufacturer, component, summary, consequence, remedy, report date
- Highlight `park_it`, `park_outside`, or `over_the_air_update` when true
- If none exist, say the **model line** has no safety recalls

This is not a specific-vehicle result. If the user later provides a VIN, use `/v1/recalls`. For many VINs use `/v1/recalls-batch/*`.
