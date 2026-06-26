# PDF / DOCX Field Tags

DocuSeal uses embedded text tags in PDF and DOCX documents to define fillable fields. Tags are placed directly in the document text and are automatically detected when uploaded via `templates create-pdf`, `templates create-docx`, `submissions create-pdf`, or `submissions create-docx`.

Full guide: https://www.docuseal.com/guides/use-embedded-text-field-tags-in-the-pdf-to-create-a-fillable-form

## Syntax

Tags use double curly braces. Attributes are separated by semicolons:

```
{{Field Name}}
{{Field Name;type=signature}}
{{Field Name;type=date;role=First Party;required=true}}
```

## Field Types

| Type | Description |
|---|---|
| `text` | Text input (default) |
| `signature` | Signature capture |
| `initials` | Initials capture |
| `date` | Date picker |
| `datenow` | Auto-filled signing date (read-only) |
| `image` | Image upload |
| `file` | File upload |
| `payment` | Payment field |
| `stamp` | Document stamp |
| `select` | Dropdown menu |
| `checkbox` | Boolean checkbox |
| `multiple` | Multiple selection |
| `radio` | Radio button |
| `phone` | Phone number (2FA) |
| `verification` | Identity verification |
| `kba` | Knowledge-based authentication |

## Attributes

| Attribute | Description |
|---|---|
| `name` | Field name (the text before the first `;`) |
| `type` | Field type (default: `text`) |
| `role` | Signer role for multi-party signing |
| `default` | Pre-filled value |
| `required` | Required field (`true` by default) |
| `readonly` | Prevent editing (`false` by default) |
| `title` | Display label in signing UI |
| `description` | Help text in signing UI |
| `options` | Comma-separated values for select/radio/multiple |
| `option` | Single option value for radio buttons |
| `condition` | Conditional visibility: `FieldName:value` |
| `width` | Width in pixels |
| `height` | Height in pixels |
| `hidden` | Hide field (`true`/`false`) |
| `mask` | Mask sensitive data (`true`/`false`) |

## Text Formatting

| Attribute | Values |
|---|---|
| `font` | `Times`, `Helvetica`, `Courier` |
| `font_size` | Numeric value |
| `font_type` | `bold`, `italic`, `bold_italic` |
| `color` | `blue`, `red`, `black` (default) |
| `align` | `left`, `center`, `right` |
| `valign` | `top`, `center`, `bottom` |

## Type-Specific Attributes

| Attribute | Applies to | Values |
|---|---|---|
| `format` | date | `DD/MM/YYYY`, `MM/DD/YYYY` (default) |
| `format` | signature | `drawn`, `typed`, `drawn_or_typed` (default), `upload` |
| `format` | number | `usd`, `eur`, `gbp` |
| `min` / `max` | date, number | Min/max allowed value |
| `method` | verification | `aes`, `qes` |

## Examples

**Basic fields:**
```
{{Full Name}}
{{Email;title=Email Address}}
{{Sign;type=signature}}
{{Date;type=date;format=DD/MM/YYYY}}
{{Today;type=datenow}}
```

**Multi-role signing:**
```
{{Landlord Name;role=Landlord}}
{{Landlord Sign;type=signature;role=Landlord}}
{{Tenant Name;role=Tenant}}
{{Tenant Sign;type=signature;role=Tenant}}
```

**Selection fields:**
```
{{Department;type=select;options=Engineering,Sales,Marketing,HR}}
{{Priority;type=radio;option=Low}}
{{Priority;type=radio;option=Medium}}
{{Priority;type=radio;option=High}}
{{type=checkbox}} I agree to the terms
```

**Conditional fields:**
```
{{Agree;type=checkbox}}
{{Details;condition=Agree:true}}
```

**Using with CLI:**
```bash
docuseal templates create-pdf --file contract.pdf --name "Contract"
docuseal templates create-docx --file contract.docx --name "Contract"
docuseal submissions create-pdf --file contract.pdf \
  -d "submitters[0][email]=john@acme.com" \
  -d "submitters[0][role]=Tenant"
```

## Resources

- Example PDF with field tags: https://www.docuseal.com/examples/fieldtags.pdf
