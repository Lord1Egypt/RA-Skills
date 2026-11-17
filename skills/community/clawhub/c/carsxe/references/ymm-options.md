# YMM Options

Cascading year / make / model / trim / variant lists. One list per request. Not full specs — use `/v1/ymm` for specs.

```
GET https://api.carsxe.com/v1/ymm-options?key=$CARSXE_KEY&source=openclaw[&dimension={DIMENSION}][&year={YEAR}][&make={MAKE}][&model={MODEL}][&trim={TRIM}]
```

Include only filters the user provided.

`dimension` is optional: `years` | `makes` | `models` | `trims` | `variants`.

## Inferred list (no `dimension`)

| make | model | year | Returns |
| --- | --- | --- | --- |
| — | — | — | `years` |
| — | — | ✓ | `makes` |
| ✓ | — | * | `models` |
| ✓ | ✓ | * | `variants` |

Typical flow: no filters → years → add year → makes → add make → models → add model → variants.

## Notes

- Present the single returned list. Show `message` if present.
- Bulk variants (`dimension=variants` + `year` + `make`, no `model`) bills 1 unit per model. `modelCount` is the billed unit count — warn before that call.
- `trim` is a substring filter on trim/variant names only (ignored for years/makes/models).
- After the user picks a YMM, offer `/v1/ymm` for full specs.
