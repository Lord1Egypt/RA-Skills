# DOCX Dynamic Content Variables

DocuSeal supports dynamic content variables in DOCX templates. Variables are replaced with provided values when creating a submission via `submissions create-docx` using the `-d "variables[key]=value"` syntax.

Full guide: https://www.docuseal.com/guides/use-dynamic-content-variables-in-docx-to-create-personalized-documents

## Syntax

Variables use double-bracket notation: `[[variable_name]]`

## Simple Variables

```
[[signer_name]]
[[company_name]]
[[contract_date]]
```

Replaced with the corresponding value passed via `variables`.

## Conditional Logic

**If:**
```
[[if:is_vip]] Thank you for being a valued VIP customer! [[end]]
```

**If/else:**
```
[[if:is_vip]] Thank you for being a valued VIP customer! [[else]] Thank you for being our customer. [[end:is_vip]]
```

The condition variable is a boolean.

## Loops

Iterate over arrays using `[[for:array_name]]`:

```
[[for:items]] - [[item.name]] ([[item.quantity]]) [[end]]
```

Table rows:
```
[[for:invoices]]
| [[invoice.name]] | [[invoice.quantity]] | [[invoice.price]] | [[invoice.total]] |
[[end]]
```

Inside the loop, access properties via singular dot notation: `items` array → `item.name`.

## HTML Content Variables

Variable values can contain styled HTML rendered directly in the DOCX:

**Paragraphs:**
```html
<p><b style="color: #1976D2; text-decoration: underline;">Bold blue text</b> normal text.</p>
```

**Lists:**
```html
<ul>
  <li>Item one</li>
  <li>Item two</li>
</ul>
```

**Tables:**
```html
<table border="1" style="border-collapse: collapse;">
  <tr><th style="padding: 8px;"><b>Item</b></th><th><b>Price</b></th></tr>
  <tr><td style="padding: 8px;">Widget</td><td>$50</td></tr>
</table>
```

**Links:**
```html
<a href="https://example.com" style="color: #1976D2;">Example Link</a>
```

## Using with CLI

```bash
# Simple variables
docuseal submissions create-docx --file contract.docx \
  -d "submitters[0][email]=john@acme.com" \
  -d "variables[signer_name]=John Doe" \
  -d "variables[company_name]=Acme Corp"

# Boolean for conditionals
docuseal submissions create-docx --file contract.docx \
  -d "submitters[0][email]=john@acme.com" \
  -d "variables[is_vip]=true"

# HTML content
docuseal submissions create-docx --file contract.docx \
  -d "submitters[0][email]=john@acme.com" \
  -d 'variables[description]=<p><b>Important</b> details here.</p>'
```
