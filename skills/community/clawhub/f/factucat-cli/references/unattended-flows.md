# Unattended flows

Use these for agents, scripts, and deterministic automation. Prefer `--json` and `--no-input`.

## Create a draft

```bash
factucat invoice create --json
```

## Set receiver

```bash
factucat invoice set-receiver \
  --draft-id dft_123 \
  --rfc XAXX010101000 \
  --legal-name "Público en general" \
  --postal-code 06000 \
  --tax-regime 616 \
  --json
```

## Set metadata

```bash
factucat invoice set-meta \
  --draft-id dft_123 \
  --cfdi-use S01 \
  --payment-method PUE \
  --payment-form 01 \
  --currency MXN \
  --json
```

If the invoice should use USD and you want automatic DOF resolution, omit `--exchange-rate`.

## Add a concept

```bash
factucat invoice add-item \
  --draft-id dft_123 \
  --description "Servicios de consultoría" \
  --quantity 1 \
  --unit-price 1000 \
  --iva 16 \
  --isr-retenido 10 \
  --json
```

## Preview

```bash
factucat invoice show --draft-id dft_123 --json
```

## Stamp

```bash
factucat invoice stamp --draft-id dft_123 --no-input --json
```

Request delivery through customer contacts:

```bash
factucat invoice stamp \
  --draft-id dft_123 \
  --send-to-customer-contacts \
  --no-input \
  --json
```

Or request specific channels:

```bash
factucat invoice stamp \
  --draft-id dft_123 \
  --send-customer-email \
  --send-customer-whatsapp \
  --no-input \
  --json
```

## Issued invoice artifacts

These commands accept a UUID or folio reference:

```bash
factucat invoice get MIAU-00036 --json
factucat invoice download xml MIAU-00036 --output ./artifacts/
factucat invoice download pdf MIAU-00036 --output ./artifacts/
```
