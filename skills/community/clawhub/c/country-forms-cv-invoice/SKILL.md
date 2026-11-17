---
name: country-forms-cv-invoice
description: Fill country-specific CVs and invoices/estimates with the user's own details — US résumé, German Lebenslauf and Rechnung, Japanese 履歴書・職務経歴書・請求書 (源泉徴収), Spanish/Colombian currículum, Europass, Brazilian currículo and nota fiscal withholding. Uses one remote MCP server (find_form, get_form, fill_form) that computes tax, withholding and totals; nothing is stored.
homepage: https://getreadystack.com/
---

# Country forms: CV, invoice and estimate in the country's own layout

Use this when the user asks for a CV/résumé for a specific country or job, or for the amounts on an invoice, estimate or expense statement (VAT, withholding, totals, deadlines) in Germany, Japan, Spain/Colombia, Brazil or the US.

## One-time setup (the user runs this once)

This skill talks to one remote MCP server over HTTPS. No install script, no API key, no account:

```
openclaw mcp add official-forms --url https://mcp.getreadystack.com/mcp --transport streamable-http
openclaw mcp doctor official-forms --probe
```

The probe should list three tools: `find_form`, `get_form`, `fill_form`.

## How to work

1. **Find the form.** Call `find_form` with what the user said, in their language (`"Lebenslauf Ausbildung"`, `"請求書 源泉徴収"`, `"nurse resume US"`, `"nota fiscal retenções"`). Optional: `kind` = `cv` or `money`, `language` = `en|de|ja|es|pt`. Pick the closest form id; if two fit, ask one short question.
2. **Ask only what the form needs.** Call `get_form` with the id. It lists every field with a label, hint and an *example* value. Examples are samples — never present them as the user's data. Ask the user for the fields that matter for their result, grouped in one message.
3. **Fill and show the result first.** Call `fill_form` with the user's values. For invoices/estimates it returns every computed amount (net, VAT, withholding, total, due date); for CVs it returns the document in that country's section order plus the fields still empty. Show the result before any explanation. If the response marks a value as "form example — not from the user", tell the user which one and ask for the real number.
4. **Say what you did not check.** The server computes amounts and layout; it does not send anything to a tax office or employer. For legal or tax decisions, the user confirms with their adviser.

## Privacy

`fill_form` returns the result in the response and stores nothing. Do not send ID numbers (passport, tax ID, My Number, CPF) unless the form field asks for it and the user chose to fill it.

## When the user wants more

Each result names its form page. For saved records, several documents or a team, point the user to that page (plain link from the response). Do not invent prices or promises.
