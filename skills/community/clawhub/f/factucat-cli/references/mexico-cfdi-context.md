# Mexican CFDI 4.0 context

FactuCat is for **Mexican CFDI 4.0 invoicing**. Use Mexican fiscal terminology when describing flows, prompts, and examples.

## Core terms

- **CFDI**: The Mexican electronic tax invoice format.
- **Timbrar**: Stamp the invoice through the authorized flow so it becomes a valid fiscal document.
- **RFC**: Mexican taxpayer identifier.
- **Razón social**: Legal name of the receiver or issuer.
- **Régimen fiscal**: SAT tax regime code for the receiver.
- **Uso CFDI**: The SAT code describing the intended use of the invoice.
- **Forma de pago**: Payment form, such as cash, transfer, or card.
- **Método de pago**: Payment method, commonly `PUE` or `PPD`.
- **XML**: Canonical stamped CFDI artifact.
- **PDF**: Human-readable representation derived from the stamped XML.

## Operational reminders

- Do not describe FactuCat as a generic invoicing CLI.
- Do not replace SAT terms with foreign-tax wording when a CFDI term already exists.
- If a user does not know the SAT details, keep the explanation simple and action-oriented.
- If a flow needs more fiscal context, prefer brief definitions over a long tax lecture.
