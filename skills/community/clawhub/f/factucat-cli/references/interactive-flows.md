# Interactive flows

Use these when a human is in the terminal and guided interaction is helpful.

## Create a draft

```bash
factucat invoice create
```

Create a draft and resolve a customer automatically:

```bash
factucat invoice create --customer "Donde nacen las ideas"
```

## Add concepts

```bash
factucat invoice add-item \
  --description "Desarrollo de sistema de facturación" \
  --unit-price 10000
```

FactuCat can infer SAT product code, SAT unit code, IVA, and retained ISR if omitted.

## Set metadata

```bash
factucat invoice set-meta \
  --cfdi-use G03 \
  --payment-method PUE \
  --payment-form 03
```

If the invoice uses USD and no exchange rate is provided:

```bash
factucat invoice set-meta --currency USD
```

FactuCat consults the official DOF exchange rate automatically.

## Review before timbrado

```bash
factucat invoice show
```

This is the full preview of the draft.

## Stamp interactively

```bash
factucat invoice stamp
```

In an interactive terminal, the CLI shows the full preview and can ask whether the stamped invoice should be sent through registered customer channels such as email or WhatsApp.
