# Liquid in DocSpring HTML templates

DocSpring renders HTML templates with Liquid 5 plus its own tags and filters. This file covers what differs from the
Liquid you know, with output checked against DocSpring's Liquid setup.

## Contents

- How data reaches Liquid
- Lax mode in submissions, strict mode in the editor
- DocSpring tags: `signature`, `initials`, `template_image_url`, `metadata`, `template`
- DocSpring filters: `currency`, `delimited`, `pluralize`, `in_time_zone`
- Standard Liquid: what works and what trips people up
- Images and barcodes
- Patterns: line items, totals, optional sections, check boxes

## How data reaches Liquid

- Each top-level key of the submission's `data` is a variable: `{{ invoice_number }}`. Nested objects use dots
  (`{{ customer.address.city }}`) and lists use indexes or loops (`{{ items[0].price }}`, `{{ items.size }}`,
  `{{ items.first.price }}`).
- Keys with spaces or dashes, or that start with a digit, use brackets: `{{ ["First Name"] }}`,
  `{{ customer["zip-code"] }}`.
- Values print as they were sent. A PDF template's field settings that format values (date formats, decimal places,
  formulas) don't apply to HTML templates: format values with filters.
- An optional field that a submission leaves out gets its field's `default`. Without a default, an optional `number`
  field becomes `0` and an optional `boolean` field `false`; other types stay empty. `0` is truthy in Liquid, so test
  numbers with `{% if discount > 0 %}`, not `{% if discount %}`.
- The same data reaches `header_html` and `footer_html`.

## Lax mode in submissions, strict mode in the editor

Submissions (from the API, forms and the MCP tools) render in lax mode:

| You write                               | Result                                                                                    |
| --------------------------------------- | ----------------------------------------------------------------------------------------- |
| `{{ missing }}`                         | Prints nothing                                                                            |
| `{{ total \| money }}`                  | The filter doesn't exist: prints the value unchanged, no error                            |
| `{{ data \| json }}`                    | No `json` filter: prints Ruby's `{"a" => 1}`                                              |
| `{% unknown_tag %}`                     | The submission fails (`syntax_error`)                                                     |
| `{% if x %}` without `endif`            | The submission fails (`syntax_error`)                                                     |
| `{{ name }` (unclosed)                  | The submission fails (`syntax_error`)                                                     |
| `{% include "x" %}`, `{% render "x" %}` | Prints "Liquid error (line 3): This liquid context does not allow includes." into the PDF |

A failed submission's `error_message` names the property and line, such as "Liquid syntax error in the template's
html (line 12): Unknown tag 'foo'". The same applies to `header_html` ("the template's header_html") and to SCSS
errors ("SCSS error in the template's scss (line 4): ...").

The template editor's preview renders random values for the template's fields in strict mode: every variable must be
a field, and every filter must exist. A template that works through the API can still show an error in the editor's
preview until it has a field for each variable.

## DocSpring tags

### `signature` and `initials`

```liquid
{% signature applicant_signature %}
{% signature applicant_signature, width: 240px %}
{% initials applicant_initials, preview_type: text, font-size: 18px, color: #333 %}
```

The value in `data` is one of:

- `{"base64": "<PNG or JPEG as base64>"}`: printed as `<img class="signature-image" src="data:...">`.
- `{"url": "https://..."}`: the template needs a `signature` (or `initials`) field with this name, which makes
  DocSpring download the image. Without the field, the tag prints an error message.
- `{"text": {"name": "Jane Doe", "typeface": "Dancing Script"}}`: printed as
  `<span class="signature-text">Jane Doe</span>` in that Google font, after a `<link>` that loads it. With a
  `signature` field, the typeface must be one of Dancing Script, Satisfy, Cookie, Great Vibes, Caveat, Sunshiney,
  Sedgwick Ave, Sacramento or Lovtony Script.

Options go after the field name, separated by commas: `width` and `height` for image signatures, and `font-size`
(default `16px`), `font-weight` (`normal`) and `color` (`black`) for text signatures. They become inline styles, so
style the classes (`.signature-image`, `.signature-text`, `.initials-image`, `.initials-text`) for anything else.
`preview_type: text` shows a text signature in the editor's preview instead of an image.

A missing value prints nothing. Keep these tags in the body: a text signature loads a Google Fonts stylesheet, and a
header or footer that loads a stylesheet fails the render. HTML templates can't take signature requests, so the
signature must already be in the data.

### `template_image_url`

```liquid
<img src="{% template_image_url company_logo %}" alt="Logo" style="height: 48px">
```

Prints the URL of an image uploaded in the template editor's Images tab, by the ID that tab shows. In
`header_html` and `footer_html` it prints the image as a `data:` URI instead, so it works there too. An unknown ID
prints nothing. There's no API for uploading these images: the user uploads them in the editor.

### `metadata`

```liquid
Order {% metadata order_id %}
```

Prints a value from the submission's `metadata` (the data a submission carries that isn't printed otherwise).

### `template`

```liquid
{% template id %} {% template name %} {% template version %} {% template version_published_at %}
```

Prints the template's ID (`tpl_...`), name, version and when it was published. A draft has no version, so
`version` and `version_published_at` print nothing in draft renders.

## DocSpring filters

| Filter         | Example                                                                   | Output             |
| -------------- | ------------------------------------------------------------------------- | ------------------ |
| `currency`     | `{{ 1234.5 \| currency }}`                                                | `$1,234.50`        |
|                | `{{ 1234.5 \| currency: "€", ".", "," }}`                                 | `€1.234,50`        |
|                | `{{ -5 \| currency: "$", ",", ".", "%u%n", "(%u%n)" }}`                   | `($5.00)`          |
|                | `{{ 1234.5 \| currency: "R$", ".", ",", "%n %u" }}`                       | `1.234,50 R$`      |
|                | `{{ 1.5 \| currency: "$", ",", ".", "%u%n", nil, 3 }}`                    | `$1.500`           |
| `delimited`    | `{{ 1234567 \| delimited }}`                                              | `1,234,567`        |
|                | `{{ 1000.45 \| delimited: ".", "," }}`                                    | `1.000,45`         |
| `pluralize`    | `{{ count }} {{ count \| pluralize: "item" }}`                            | `2 items`          |
|                | `{{ 1 \| pluralize: "city", "cities" }}`                                  | `city`             |
| `in_time_zone` | `{{ "now" \| in_time_zone: "Europe/London" \| date: "%-d %B %Y %H:%M" }}` | The time in London |

- `currency` takes, in order: unit (default `$`), thousands delimiter (`,`), decimal separator (`.`), format (`%u%n`),
  negative format (`nil` keeps the default), precision (`2`, a number, not a string). It accepts numbers sent as
  strings, but prints a non-number as it is (`"abc"` prints `$abc`).
- `pluralize` prints only the word, not the count.
- `in_time_zone` takes `"now"`, `"today"`, or a date or time. Give times an offset (`2026-05-01T09:00:00Z`): a time
  without one is read in the account's time zone (templates created before 29 October 2026: US Eastern), and a date
  on its own can shift to the day before. An unknown zone name is ignored. Zone names are the IANA ones
  (`America/New_York`):
  `https://docspring.com/docs/html-templates/liquid-timezones/`.

More examples: `https://docspring.com/docs/html-templates/liquid-filters/`.

## Standard Liquid: what works and what trips people up

Everything in standard Liquid 5 works except `include` and `render`: `if`/`elsif`/`unless`/`case`, `for` (with
`limit`, `offset`, `reversed` and `forloop`), `cycle`, `tablerow`, `assign`, `capture`, `comment`, `raw`, `liquid`
and `echo`, and filters such as `date`, `default`, `escape`, `newline_to_br`, `strip_html`, `upcase`, `truncate`,
`replace`, `split`, `join`, `map`, `where`, `sort`, `sum`, `plus`, `times`, `divided_by`, `round`.

- **Escaping:** a template with `html_escape_data` on (new templates) prints `{{ value }}` as text and
  `{{ value | raw }}` as HTML. One with it off (templates from before October 2026) inserts every value as HTML: use
  `| escape` on free text there. `| escape` is never escaped twice, so it's safe in both.
- **Line breaks** in a value don't show in HTML: `{{ address | escape | newline_to_br }}`.
- **Dates:** `date` reads `03/05/2026` as 3 May 2026 (day first). Send ISO dates (`2026-03-05`) and format them:
  `{{ due_date | date: "%B %-d, %Y" }}` prints `March 5, 2026`.
- **Truthiness:** only `nil` and `false` are false. `0`, `""` and `"false"` are true. Test text with
  `{% if notes != blank %}` and numbers with `> 0`.
- **`default`** replaces `false` too: `{{ subscribed | default: true }}` prints `true` when `subscribed` is `false`.
- **Integer division:** `{{ 10 | divided_by: 4 }}` is `2`; write `divided_by: 4.0` for `2.5`.
- **Numbers sent as strings** can't be compared: `{% if n > 5 %}` prints "Liquid error (line 3): comparison of String
  with 5 failed" into the PDF. Convert first: `{% assign n = n | plus: 0 %}`.
- **Rounding money:** `round: 2` gives `12.35` but drops trailing zeros (`12.5`); use `currency` to print amounts.

## Images and barcodes

- **Image fields.** Give the template an `image` field (`photo`, or `items/~/photo` inside a list), send
  `{"url": "https://..."}` or `{"base64": "..."}`, and print `<img src="{{ photo }}">`. DocSpring downloads and
  stores the image and prints its URL (in headers and footers, a `data:` URI). A URL that can't be downloaded fails
  the submission (`image_download_failed`); a file that isn't an image fails it too (`image_processing_failed`).
- **Optional images:** `{% if photo %}<img src="{{ photo }}">{% endif %}`.
- **Size:** set a CSS width or height on the `<img>`, and resize large photos before sending them: a PDF over the
  size limit fails.
- **Barcodes.** Give the template a `barcode` field and send the text to encode. `{{ tracking_code }}` prints the URL
  of a PNG of the barcode: `<img src="{{ tracking_code }}" style="height: 40px">`. The field's `barcode_symbology`
  (default `code_128`) sets the format. There's no QR code field: make the QR code image in the user's app and send
  it to an image field.

## Patterns

Line items with a subtotal, a table header that repeats on each page, and rows that don't split:

```liquid
<table class="items">
  <thead><tr><th>Item</th><th class="num">Qty</th><th class="num">Price</th><th class="num">Amount</th></tr></thead>
  <tbody>
    {% assign subtotal = 0 %}
    {% for item in line_items %}
      {% assign amount = item.quantity | times: item.unit_price %}
      {% assign subtotal = subtotal | plus: amount %}
      <tr>
        <td>{{ item.description | escape }}</td>
        <td class="num">{{ item.quantity }}</td>
        <td class="num">{{ item.unit_price | currency }}</td>
        <td class="num">{{ amount | currency }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
<p class="total">Subtotal: {{ subtotal | currency }}</p>
```

```scss
.items {
  width: 100%;
  border-collapse: collapse;
}
.items tr {
  break-inside: avoid;
}
.num {
  text-align: right;
}
```

The fields for this data are `line_items/~/description`, `line_items/~/quantity` (number) and
`line_items/~/unit_price` (number).

An optional section:

```liquid
{% if notes != blank %}
  <section class="notes"><h2>Notes</h2><p>{{ notes | escape | newline_to_br }}</p></section>
{% endif %}
```

A check box from a boolean:

```liquid
<span class="box">{% if agreed_to_terms %}&#9746;{% else %}&#9744;{% endif %}</span> I agree to the terms
```

A value chosen from a list (a field with an `option_list`):

```liquid
{% case plan %}{% when "pro" %}Pro plan{% when "basic" %}Basic plan{% else %}{{ plan | escape }}{% endcase %}
```
