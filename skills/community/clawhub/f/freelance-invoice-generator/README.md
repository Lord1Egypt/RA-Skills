# Freelance Invoice Generator

A zero-dependency Python tool that renders a JSON job description into a
clean Markdown or HTML invoice.

## What it does

- Computes subtotal, discount, tax, and total from a list of line items
- Renders a formatted Markdown invoice or a styled standalone HTML invoice
- Includes optional late-fee and notes sections

## Quick start

```bash
python3 scripts/invoice_gen.py job.json --out invoice.md
python3 scripts/invoice_gen.py job.json --out invoice.html --format html
```

See `SKILL.md` for the full job JSON schema.

## Dependencies

Standard library only — no `pip install` required.

## Notes

To produce a PDF, pipe the Markdown output through `pandoc` if it's
available in your environment: `pandoc invoice.md -o invoice.pdf`.
