# Print CSS for DocSpring HTML templates

How DocSpring's renderer turns a template into pages, and how to get headers, footers, page breaks and fonts right.
Each behaviour here was checked by rendering pages the way DocSpring does.

## Contents

- How a template is printed
- Page settings
- Headers and footers
- Page breaks and long tables
- Fonts
- Backgrounds and full-bleed designs
- Images
- Limits, and renders that fail
- A starter template

## How a template is printed

1. DocSpring renders the Liquid in `html` with the submission's data, and compiles the SCSS.
2. It builds the page: normalize.css, then DocSpring's default CSS
   (`html, body { font-family: Arial, sans-serif; font-size: 12px; }`
   `body { background: white; -webkit-print-color-adjust: exact; }`), then the template's SCSS, then the HTML.
3. Headless Chrome loads the page, waits until the network is idle and the fonts have loaded, and prints it with the
   template's `html_engine_options`. `header_html` and `footer_html` print in the margins of every page.

Chrome prints with print media, so `@media print` rules apply. A CSS pixel is 1/96 inch: on Letter paper with 1in
margins, the body is 6.5in (624px) wide; on A4 with 20mm margins it's about 170mm (643px).

## Page settings

`html_engine_options` is replaced whole by `update_template` (or `PUT /templates/{template_id}`): send every option.

A4 with 20mm margins:

```json
{
  "format": "A4",
  "landscape": false,
  "scale": 1,
  "print_background": false,
  "margin_top": "20mm",
  "margin_bottom": "20mm",
  "margin_left": "20mm",
  "margin_right": "20mm"
}
```

A 4 × 6 inch label (a `Custom` page takes `width` and `height`; leave `landscape` off):

```json
{
  "format": "Custom",
  "width": "4in",
  "height": "6in",
  "landscape": false,
  "scale": 1,
  "print_background": false,
  "margin_top": "0.25in",
  "margin_bottom": "0.25in",
  "margin_left": "0.25in",
  "margin_right": "0.25in"
}
```

- Lengths take `in`, `cm`, `mm` or `px`. Other units, such as `pt` or `em`, don't work.
- Matching a PDF template's page: its `document.page_dimensions` are in points (72 a inch). 612 × 792 is Letter,
  595 × 842 is A4; anything else is `Custom` with the size in inches (points ÷ 72).
- Don't use CSS `@page` for size or margins. An `@page` size doesn't set the paper size (only its orientation turns
  the page), and `@page` margins override `html_engine_options`, which takes the header and footer's room away.
- `scale` shrinks or enlarges the body's content, such as `0.9` to fit a wide table. Fix the CSS first.

## Headers and footers

Chrome prints `header_html` in the top margin and `footer_html` in the bottom margin of every page, each as its own
small document. What that means:

- **Styles.** They get DocSpring's default CSS (Arial 12px, `-webkit-print-color-adjust: exact`) and the template's
  SCSS, so classes you define in the SCSS work in them. They don't get normalize.css, and nothing the body loads
  (`<link>` stylesheets, fonts, scripts) reaches them. Because the SCSS is shared, give header and footer classes
  their own names (`.page-footer`), and remember that rules on `body` apply to them too.
- **Position.** They span the paper's full width from its left edge: give them `box-sizing: border-box`,
  `width: 100%` and side padding equal to the body's side margins. Chrome already puts the header a little below
  the paper's top edge and the footer a little above its bottom edge, so don't pad them towards the body: check the
  gap on the rendered pages, and raise the margin if it's too small.
- **Room.** They must fit inside `margin_top` and `margin_bottom`. A taller header overlaps the body; a `0in` margin
  hides it. Raise the margin, or make the header smaller.
- **Page numbers.** Elements with the classes `pageNumber` and `totalPages` get the page number and the page count.
- **Liquid** works with the same data as the body.
- **Images.** Only `data:` URIs display. An `image` field's value (`{{ logo }}`) and `{% template_image_url ID %}`
  become `data:` URIs automatically in headers and footers (each image up to 25 MB). A plain `https://` image URL, or
  a CSS `background-image` URL, prints nothing.
- **Fonts.** Use an installed font (see Fonts), or a font that the SCSS declares with `@font-face` and a base64
  `data:` URL **and** that some text in the body uses: the header can only use a font the body has already loaded.
  Never load anything from the network in a header or footer: a `<link rel="stylesheet">`, an `@import`, or a font
  whose `@font-face` points at a URL makes the whole render fail, with an `error_message` that starts "The header or
  footer couldn't be printed". A typed `{% signature %}` adds a Google Fonts `<link>`, so keep signatures in the body.
- **Content that needs a web font or a linked image on every page** can go in the body instead, as an element with
  `position: fixed`: Chrome repeats it on every page, inside the margins. It sits over the content, so leave room for
  it, and it can't show page numbers.

A footer with page numbers (the starter template below has its SCSS):

```liquid
<div class="page-footer">
  <span>{{ company.name | escape }} · {{ invoice_number | escape }}</span>
  <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
</div>
```

A header with a logo uploaded in the editor's Images tab (it fits a `0.75in` top margin):

```liquid
<div class="page-header">
  <img src="{% template_image_url company_logo %}" style="height: 28px" />
  <span>{{ document_title | escape }}</span>
</div>
```

```scss
.page-header {
  box-sizing: border-box;
  width: 100%;
  padding: 0 0.75in;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 9px;
}
```

## Page breaks and long tables

- Start a new page: `break-before: page` (or `page-break-before: always`) on the element.
- Keep something together: `break-inside: avoid` on table rows, signature blocks and figures. A block taller than a
  page breaks anyway.
- Tables: Chrome repeats `<thead>` at the top and `<tfoot>` at the bottom of every page a table runs over. Put column
  headings in `<thead>`, and never totals in `<tfoot>`: they'd print on every page.
- **Keep totals with the last rows.** A totals block after the table, with `break-inside: avoid`, moves to the next
  page on its own whenever it doesn't fit under the last row. Make the totals the last row of the same `<tbody>` as the
  line items (one row, with a small table of its own in a cell), and give the last line item `break-after: avoid`:
  Chrome then carries that line item over with the totals. A second `<tbody>` doesn't work: Chrome ignores
  `break-inside: avoid` on it and splits the totals across pages. The starter template below does this.
- **Use `border-collapse: separate`** (with `border-spacing: 0`) on a table that can run over pages. With `collapse`,
  the header row loses its borders where `<thead>` repeats on the next page.
- `orphans` and `widows` work on paragraphs.
- An empty last page usually comes from `break-after: page` on the last element, or from an element as tall as the
  paper (`height: 11in`, `100vh`) in a page with margins. Make full-page blocks the page's height minus its margins.
- Test page breaks with data long enough to fill two or three pages, and look at every page.

## Fonts

- **Installed:** the Liberation fonts (metric-compatible with Arial, Times New Roman and Courier New), Noto Sans,
  Noto Serif, Noto Sans CJK and Noto Color Emoji. `font-family: Arial, sans-serif` (the default) is safe. Other names
  fall back to one of these: fonts installed on your machine or the user's aren't on the renderer.
- **Web fonts in the body:** a `<link>` in the `html`, with every weight you use:

  ```html
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
    rel="stylesheet"
  />
  ```

  Or an `@font-face` in the SCSS whose `src` is an `https://` URL or a base64 `data:` URL. An `@import url(...)` in
  the SCSS is ignored: it ends up after DocSpring's own CSS, where Chrome drops it.

- **Fonts in headers and footers:** see Headers and footers.
- A font that fails to load falls back without an error: look at the rendered pages to check it.

## Backgrounds and full-bleed designs

- Element backgrounds (`background` on a `div`, table cell or heading) print with `print_background` off, because
  the default CSS sets `-webkit-print-color-adjust: exact` on `body`.
- A background on `html` or `body` prints only with `print_background: true`, and only inside the margins.
- Nothing prints in the margins except the header and footer. For a design that reaches the paper's edges (a
  coloured cover, a certificate border), set every margin to `0in`, and pad the content yourself. With `0in` margins
  there's no room for `header_html` or `footer_html`.
- A full-page block on a `0in`-margin Letter page is `height: 11in` (`297mm` on A4); use `box-sizing: border-box` so
  its padding doesn't push it onto a second page.

## Images

- In the body, `<img>` loads `https://` URLs, `data:` URIs, `image` field values and `{% template_image_url ID %}`.
- The renderer blocks DocSpring's own app domains (its signed `downloads.docspring.com` links work), private network
  addresses and `file://` URLs. A blocked or missing image prints nothing.
- Size images with CSS (`width`, `height`, `max-width: 100%`, `object-fit`), and resize photos to about the size they
  print at before sending them: full-size camera photos make huge PDFs.
- SVG works inline (`<svg>...</svg>`) and as a `data:image/svg+xml` URI.

## Limits, and renders that fail

The limits (`https://docspring.com/docs/html-templates/overview/#limits`): a generated PDF up to 500 MB, up to 128 MB
of HTML in total for the body, header and footer (including base64 images), header and footer images up to 25 MB each,
and image field URLs up to 100 MB each. A render also has a time limit of under a minute.

| What you see                                                    | Likely cause and fix                                                                                             |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| State `syntax_error`                                            | A Liquid or SCSS error: `error_message` names the property and line.                                             |
| State `image_download_failed` or `image_processing_failed`      | An image field's URL couldn't be downloaded, or isn't an image.                                                  |
| "The page didn't finish loading" or "took too long to render"   | A URL in the HTML or data is slow or unreachable, or the document is too big. Remove the URL; resize the images. |
| "The header or footer couldn't be printed" in the error message | The header or footer loads a stylesheet or a web font. Inline the CSS, and use an installed or `data:` font.     |
| Header or footer missing                                        | Margin too small or `0in`, or an `@page` margin in the SCSS.                                                     |
| Header or footer overlaps the body                              | It's taller than its margin: raise `margin_top` or `margin_bottom`.                                              |
| Layout differs from a browser, odd table or line heights        | Quirks mode: the `html` has a doctype but no plain `<head>`. Use a fragment, or add `<head>`.                    |
| Web font missing                                                | `@import` in the SCSS, a missing weight in the font URL, or a header/footer using a font the body doesn't load.  |
| Blank values                                                    | A misspelt variable or a value missing from the data: lax mode prints nothing. Check the data keys.              |

## A starter template

An invoice that runs onto as many pages as its line items need, with a footer and page numbers. Rendered and checked
with 3 to 92 line items: the header row repeats on every page, and the totals stay with the last line item.

`html`:

```liquid
<header class="doc-header">
  <div>
    <h1>Invoice</h1>
    <p class="muted">{{ invoice_number | escape }} · Issued {{ issue_date | date: "%B %-d, %Y" }}</p>
  </div>
  <div class="from">
    <strong>{{ company.name | escape }}</strong><br>
    {{ company.address | escape | newline_to_br }}
  </div>
</header>

<section class="bill-to">
  <h2>Bill to</h2>
  <p><strong>{{ customer.name | escape }}</strong><br>{{ customer.address | escape | newline_to_br }}</p>
</section>

<table class="items">
  <thead>
    <tr><th>Description</th><th class="num">Qty</th><th class="num">Unit price</th><th class="num">Amount</th></tr>
  </thead>
  <tbody>
    {% assign subtotal = 0 %}
    {% for item in line_items %}
      {% assign amount = item.quantity | times: item.unit_price %}
      {% assign subtotal = subtotal | plus: amount %}
      <tr class="line{% if forloop.last %} last-line{% endif %}">
        <td>{{ item.description | escape }}</td>
        <td class="num">{{ item.quantity }}</td>
        <td class="num">{{ item.unit_price | currency }}</td>
        <td class="num">{{ amount | currency }}</td>
      </tr>
    {% endfor %}
    {% assign tax = subtotal | times: tax_rate | divided_by: 100.0 %}
    <tr class="totals-row">
      <td colspan="2"></td>
      <td colspan="2">
        <table class="totals">
          <tr><th>Subtotal</th><td class="num">{{ subtotal | currency }}</td></tr>
          {% if tax_rate > 0 %}<tr><th>Tax ({{ tax_rate }}%)</th><td class="num">{{ tax | currency }}</td></tr>{% endif %}
          <tr class="grand"><th>Total</th><td class="num">{{ subtotal | plus: tax | currency }}</td></tr>
        </table>
      </td>
    </tr>
  </tbody>
</table>

{% if notes != blank %}
  <section class="notes"><h2>Notes</h2><p>{{ notes | escape | newline_to_br }}</p></section>
{% endif %}
```

`scss`:

```scss
$ink: #1f2937;
$muted: #6b7280;
$rule: #e5e7eb;

body {
  color: $ink;
  font-size: 11px;
  line-height: 1.45;
}
h1 {
  font-size: 24px;
  margin: 0 0 4px;
}
h2 {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: $muted;
  margin: 0 0 4px;
}
.muted {
  color: $muted;
  margin: 0;
}
.doc-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
}
.from {
  text-align: right;
}
.bill-to {
  margin-bottom: 20px;
}
// separate, not collapse: with collapse, the header row loses its border where it repeats on the next page
table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}
th {
  text-align: left;
}
.items thead th {
  border-bottom: 1px solid $ink;
  padding: 6px 4px;
}
.line td {
  border-bottom: 1px solid $rule;
  padding: 6px 4px;
  vertical-align: top;
}
.items tr {
  break-inside: avoid;
}
.num {
  text-align: right;
  white-space: nowrap;
}
// The totals are the last row of the same tbody: this carries the last line item over with them
.last-line {
  break-after: avoid;
}
.totals-row > td {
  padding: 12px 0 0;
}
// nowrap: a long label ("Total (NZD)") would wrap in the narrow last columns
.totals th,
.totals td {
  font-weight: normal;
  padding: 3px 4px;
  white-space: nowrap;
}
.totals .grand th,
.totals .grand td {
  font-weight: bold;
  border-top: 1px solid $ink;
  padding-top: 6px;
}
.notes {
  margin-top: 28px;
  break-inside: avoid;
}

// The footer (footer_html): it starts at the paper's edge, so pad it to the body's side margins
.page-footer {
  box-sizing: border-box;
  width: 100%;
  padding: 0 0.75in;
  display: flex;
  justify-content: space-between;
  font-size: 8px;
  color: $muted;
}
```

`footer_html`: the page-number footer under Headers and footers.

`html_engine_options`: `Letter`, every margin `0.75in`, everything else at its default.

Fields: `invoice_number`, `issue_date` (date), `tax_rate` (number, optional), `company/name`, `company/address`,
`customer/name`, `customer/address`, `line_items/~/description`, `line_items/~/quantity` (number),
`line_items/~/unit_price` (number) and `notes` (optional).
