# HTML Field Tags

DocuSeal uses custom HTML tags to define fillable fields in templates. These tags can be used in `--html` or `--file` values for `templates create-html` and `submissions create-html` commands.

Full guide: https://www.docuseal.com/guides/create-pdf-document-fillable-form-with-html-api

## Available Tags

| Tag | Purpose |
|---|---|
| `<text-field>` | Text input |
| `<signature-field>` | Signature capture |
| `<date-field>` | Date picker |
| `<image-field>` | Image upload |
| `<initials-field>` | Initials capture |
| `<phone-field>` | Phone number input |
| `<stamp-field>` | Document stamp |
| `<file-field>` | File attachment |
| `<checkbox-field>` | Boolean checkbox |
| `<radio-field>` | Single option selection |
| `<select-field>` | Dropdown menu |
| `<multi-select-field>` | Multiple selection dropdown |
| `<payment-field>` | Payment processing |
| `<verification-field>` | Identity verification |

## Common Attributes

All tags support:

| Attribute | Description |
|---|---|
| `name` | Field identifier (required) |
| `role` | Signer role assignment |
| `default` | Pre-filled value |
| `required` | Required field, `true` by default |
| `readonly` | Prevent editing by signer |
| `title` | Display label |
| `description` | Help text shown to signer |
| `condition` | Conditional visibility, e.g. `"Status:active"` |
| `style` | CSS styling for field size and placement. Set `width` and `height` so the field renders on the page. |

**Important:** HTML field tags should usually include a `style` attribute with at least `width` and `height`. Without explicit dimensions, the rendered field can collapse and not appear where you expect in the document. For inline fields, `display: inline-block` is commonly used.

## Style Examples

Use `style=""` to control field size and layout:

```html
<text-field name="Full Name" role="Tenant" style="width: 160px; height: 20px; display: inline-block;"></text-field>
<signature-field name="Tenant Signature" role="Tenant" style="width: 160px; height: 80px; display: inline-block;"></signature-field>
```

## Text Formatting Attributes

| Attribute | Values |
|---|---|
| `font` | `Times`, `Helvetica`, `Courier` |
| `font-size` | Numeric value |
| `font-type` | `bold`, `italic`, `bold_italic` |
| `color` | `blue`, `red`, `black` (default) |
| `align` | `left`, `center`, `right` |
| `valign` | `top`, `center`, `bottom` |
| `mask` | `true` / `false` (hide sensitive data) |

## Type-Specific Attributes

**`<select-field>`, `<multi-select-field>`, `<radio-field>`:**

| Attribute | Description |
|---|---|
| `options` | Comma-separated list: `"opt1,opt2,opt3"` |

**`<date-field>`:**

| Attribute | Description |
|---|---|
| `min` / `max` | Min/max date |
| `format` | `DD/MM/YYYY` or `MM/DD/YYYY` |

**`<signature-field>`:**

| Attribute | Description |
|---|---|
| `format` | `drawn`, `typed`, `drawn_or_typed`, `upload` |

**`<payment-field>`:**

| Attribute | Description |
|---|---|
| `price` | Amount |
| `currency` | Currency code (e.g. `USD`) |

**`<verification-field>`:**

| Attribute | Description |
|---|---|
| `method` | `aes` or `qes` |

## Examples

**Simple contract:**
```html
<h1>Non-Disclosure Agreement</h1>
<p>This agreement is entered by
  <text-field name="Company Name" role="Company" style="width: 180px; height: 20px; display: inline-block;"></text-field>
  and
  <text-field name="Recipient Name" role="Recipient" style="width: 180px; height: 20px; display: inline-block;"></text-field>.
</p>

<p>Date:
  <date-field name="Date" format="MM/DD/YYYY" style="width: 110px; height: 20px; display: inline-block;"></date-field>
</p>

<p>Company signature:</p>
<signature-field name="Company Signature" role="Company" style="width: 180px; height: 80px; display: inline-block;"></signature-field>

<p>Recipient signature:</p>
<signature-field name="Recipient Signature" role="Recipient" style="width: 180px; height: 80px; display: inline-block;"></signature-field>
```

**Form with various field types:**
```html
<h2>Application Form</h2>
<p>Full Name: <text-field name="Full Name" required="true" style="width: 220px; height: 20px; display: inline-block;"></text-field></p>
<p>Phone: <phone-field name="Phone" style="width: 160px; height: 20px; display: inline-block;"></phone-field></p>
<p>Department: <select-field name="Department" options="Engineering,Sales,Marketing,HR" style="width: 180px; height: 24px; display: inline-block;"></select-field></p>
<p>Start Date: <date-field name="Start Date" min="2024-01-01" style="width: 120px; height: 20px; display: inline-block;"></date-field></p>
<p>Photo ID: <image-field name="Photo ID" style="width: 140px; height: 90px; display: inline-block;"></image-field></p>
<p>I agree to the terms: <checkbox-field name="Terms" required="true" style="width: 16px; height: 16px; display: inline-block;"></checkbox-field></p>
<signature-field name="Signature" style="width: 180px; height: 80px; display: inline-block;"></signature-field>
```

**Using with CLI:**
```bash
docuseal templates create-html --name "NDA" --html '<h1>NDA</h1>
<p>Party: <text-field name="Name" style="width: 180px; height: 20px; display: inline-block;"></text-field></p>
<signature-field name="Signature" style="width: 180px; height: 80px; display: inline-block;"></signature-field>'

docuseal templates create-html --name "NDA" --file nda.html

docuseal submissions create-html --file nda.html \
  -d "submitters[0][email]=john@acme.com"
```
