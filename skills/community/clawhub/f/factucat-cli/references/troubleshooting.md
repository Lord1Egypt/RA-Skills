# Troubleshooting

## Invalid API key

Symptom:

- `API key inválida o revocada`

Recovery:

```bash
factucat auth api-key set
factucat auth status
```

## No active draft

Symptom:

- `No hay borrador activo`

Recovery:

```bash
factucat invoice create
```

Or explicitly select a draft:

```bash
factucat invoice use dft_123
```

## Ambiguous customer lookup

Symptom:

- `invoice create --customer "..."` cannot resolve a unique customer

Recovery:

```bash
factucat customer search "Donde nacen"
factucat invoice create --customer-id cus_123
```

## Stamp failure

Recovery:

```bash
factucat invoice show
```

Then verify receiver data, CFDI metadata, and draft concepts.

## Download path confusion

If the user does not know where the XML or PDF was saved, use an explicit destination:

```bash
factucat invoice download pdf MIAU-00036 --output ./facturas/factura.pdf
```
