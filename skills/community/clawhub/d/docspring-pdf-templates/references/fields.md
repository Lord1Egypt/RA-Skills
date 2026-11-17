# DocSpring field reference

Every field type and setting for `add_fields` and `update_fields` (and the REST API v2's field endpoints, which use
the same names), with recipes for the fields forms need most.

## Contents

1. Positions and sizes
2. Field types
3. Shared and per-field settings
4. Settings by display type
5. Recipes: checkbox, radio group, multi-choice checkboxes, signature, date in boxes, SSN boxes, multiline, combined,
   static, number with a formula, QR code and barcode, image
6. Field names
7. Conditional logic
8. Formulas

## 1. Positions and sizes

| Value      | Meaning                                                                                      |
| ---------- | -------------------------------------------------------------------------------------------- |
| `page`     | The page number, from 1. A field added without one goes on page 1.                           |
| `x`        | From the page's left edge to the field's left edge, in units. Every page is 2480 units wide. |
| `y`        | From the top of the field's page down to the field's top edge, in units.                     |
| `width`    | The field's width in units. A check mark is sized to the width.                              |
| `height`   | The field's height in units. Keep check marks, QR codes, squares and circles square.         |
| `rotation` | Degrees clockwise, -360 to 360.                                                              |

Converting:

| From                                                      | To units                               |
| --------------------------------------------------------- | -------------------------------------- |
| A pixel in `get_template_pages` or `get_submission_pages` | × 2.5 (the images are 992 pixels wide) |
| A pixel in a REST page image (`page_images`, `files.png`) | × 2480 ÷ the image's `width`           |
| A PDF point                                               | × 2480 ÷ the page's width in points    |

| Page size | Points    | Units                 | Units per point |
| --------- | --------- | --------------------- | --------------- |
| US Letter | 612 × 792 | 2480 × 3209           | about 4.05      |
| A4        | 595 × 842 | 2480 × 3508           | about 4.17      |
| Any       | w × h     | 2480 × (2480 × h ÷ w) | 2480 ÷ w        |

A new field is 300 × 55 units unless you send `width` and `height`. A field added without `y` is stacked 75 units
below the previous one, from the top of the page: always send `y`. Text prints at the bottom of its box
(`v_alignment: "bottom"`), so put the box's bottom edge on the form's line. For 11-point text on a Letter page, a box
about 55 to 65 units tall fits one line.

## 2. Field types

`type` is what the submission data sends. `display_type` is how it prints. Use only the display types listed for the
type.

| `type`      | Value in submission data                                      | `display_type`s                               | Notes                                                                                                                                                   |
| ----------- | ------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `string`    | Text                                                          | `text`, `check`, `shape`, `qrcode`, `barcode` | `option_list` limits it to a list. Radio groups use it.                                                                                                 |
| `number`    | A number                                                      | `text`, `check`, `shape`                      | `integer`, `minimum`, `maximum`, `decimal_places`, `currency`, formulas                                                                                 |
| `boolean`   | `true` or `false`                                             | `text`, `check`, `shape`                      | A check mark prints when `true`.                                                                                                                        |
| `date`      | `YYYY-MM-DD` (with `include_time`, an RFC 3339 date-time)     | `text`                                        | `date_time_format` sets how it prints. With the template's `parse_dates_using_template_date_format`, also `03/05/2026` in the order of its date format. |
| `address`   | Text                                                          | `text`                                        | Forms autocomplete addresses.                                                                                                                           |
| `country`   | Text                                                          | `text`, `check`, `shape`                      | Any text, printed as sent. Web forms offer a list of English country names.                                                                             |
| `email`     | A valid email address                                         | `text`, `qrcode`, `barcode`                   |                                                                                                                                                         |
| `url`       | A valid URL                                                   | `text`, `qrcode`, `barcode`                   |                                                                                                                                                         |
| `image`     | `{"url": "https://..."}` or `{"base64": "..."}`               | `image`                                       | `image_scale_type`, `image_gravity`                                                                                                                     |
| `signature` | As `image`, or `{"text": {"name": "...", "typeface": "..."}}` | `image`                                       | Signers fill it in through signature requests.                                                                                                          |
| `initials`  | As `signature`                                                | `image`                                       |                                                                                                                                                         |
| `barcode`   | Text that `barcode_symbology` accepts                         | `text`, `barcode`                             | `code_128` (the default) takes any ASCII.                                                                                                               |
| `combined`  | Not sent: made from other fields' values                      | `text`                                        | See the recipe.                                                                                                                                         |

A typed signature's `typeface` is one of `Dancing Script`, `Satisfy`, `Cookie`, `Great Vibes`, `Caveat`, `Sunshiney`,
`Sedgwick Ave`, `Sacramento` or `Lovtony Script`. `add_fields` doesn't stop you giving a field a display type its type
can't use, so set `display_type` yourself: `image` for `image`, `signature` and `initials`; `check` for checkboxes.

Details: [field data types](https://docspring.com/docs/reference/field-data-types/) and
[field display types](https://docspring.com/docs/reference/field-display-types/).

## 3. Shared and per-field settings

Fields with the same name share one value and these **shared settings**. Changing one with `update_fields` changes it
for every field with the name. A field added with an existing name takes them: `add_fields` refuses one that sets a
shared setting to another value, so leave them out when you add a copy.

`type`, `required` (default `true`), `default`, `title`, `description`, `placeholder`, `metadata`, `option_list`,
`static`, `editable`, `dependencies`, `integer`, `minimum`, `maximum`, `exclusive_minimum`, `exclusive_maximum`,
`include_time`, `combined_field_names`, `combined_field_type`, `combined_field_separator`, `combined_field_format`,
`signature_allow_draw`, `signature_allow_type`, `barcode_symbology`.

Everything else belongs to one field on one page, so one value can print differently in two places: the position and
size, `display_type`, `hidden`, the text style, `date_time_format`, `decimal_places`, `currency`, `min_length`,
`max_length`, the check, shape, image and QR code settings, and `condition` with its comparison settings.

| Setting                                                                   | What it does                                                                                                                             |
| ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `required`                                                                | Each submission must send a value. New fields are required unless you send `false`.                                                      |
| `default`                                                                 | Used when the data leaves the field out, and fills in forms. A number field's can be a formula; a static field's is what it prints.      |
| `title`                                                                   | The label in the data schema and on forms. Empty: made from the name.                                                                    |
| `description`                                                             | Help text in the data schema and on forms.                                                                                               |
| `placeholder`                                                             | Placeholder text on forms.                                                                                                               |
| `metadata`                                                                | Your own text, in the data schema as `x-metadata`.                                                                                       |
| `option_list`                                                             | `string` only: comma-separated accepted values. An `enum` in the data schema, a select list on forms.                                    |
| `static`                                                                  | Prints its `default` on every PDF, and leaves the field out of the data schema and forms.                                                |
| `hidden`                                                                  | Doesn't print, but stays in the data (`x-hidden`), so combined fields and rules can use it.                                              |
| `editable`                                                                | Text and check display: prints a fillable PDF form field instead of flat content.                                                        |
| `integer`, `minimum`, `maximum`, `exclusive_minimum`, `exclusive_maximum` | `number` validation.                                                                                                                     |
| `decimal_places`                                                          | `number` with text display: 0 to 99 decimal places. Empty prints the number as sent.                                                     |
| `currency`                                                                | `number`: a currency input on forms. It doesn't change how the number prints.                                                            |
| `include_time`                                                            | `date`: the value is a date and time.                                                                                                    |
| `date_time_format`                                                        | `date`: a strftime format (`%m/%d/%Y`, `%-d %B %Y`), or `@years_since` and the other `@` calculations. Empty uses the template's format. |
| `min_length`, `max_length`                                                | Text display: length limits added to the data schema.                                                                                    |
| `barcode_symbology`                                                       | `code_25`, `code_39`, `code_93`, `code_128`, `ean_13`, `ean_8`, `upc_a` or `pdf417`.                                                     |
| `signature_allow_draw`, `signature_allow_type`                            | `signature` and `initials`: let signers draw, or type their name in a script font.                                                       |

## 4. Settings by display type

**Text** (`display_type: "text"`):

| Setting                              | Values                                                                                                                                                                                                                                                                                                |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `typeface`                           | `Helvetica`, `Arial`, `Calibri`, `Open Sans`, `Roboto`, `Lato`, `Poppins`, `Public Sans`, `Questrial`, `Times New Roman`, `Dancing Script`, `Lovtony Script`, or monospace `Courier`, `Inconsolata`, `Menlo`, `Roboto Mono`, `Ubuntu Mono`. Empty: the template's default (Helvetica unless changed). |
| `font_size`                          | Whole points. Empty: the template's default (11 unless changed).                                                                                                                                                                                                                                      |
| `character_spacing`                  | Extra points between characters, 0 to 50.                                                                                                                                                                                                                                                             |
| `bold`, `uppercase`, `strikethrough` | `true` or `false`.                                                                                                                                                                                                                                                                                    |
| `color`, `background_color`          | 6 hex digits without `#` (`444444`). The background covers what the page shows behind a filled field.                                                                                                                                                                                                 |
| `alignment`                          | `left` (default), `center`, `right`, `justify`.                                                                                                                                                                                                                                                       |
| `v_alignment`                        | `bottom` (default), `center`, `top`.                                                                                                                                                                                                                                                                  |
| `overflow`                           | `shrink_to_fit` (default, down to 5 points) or `truncate` (the rest goes in the submission's `truncated_text`).                                                                                                                                                                                       |
| `multiline`                          | Wraps text over the box's height. `multiline_lines` spreads it over exactly that many lines (1 to 300), to match lines printed on the form.                                                                                                                                                           |
| `comb`                               | One character in each of `comb_number_of_cells` equal boxes; `comb_value_offset` is the first character it prints.                                                                                                                                                                                    |
| `keep_leading_spaces`                | Keeps leading spaces, to line text up.                                                                                                                                                                                                                                                                |
| `auto_calculate_max_length`          | With a monospace typeface: adds how many characters fit to the data schema as `max_length`.                                                                                                                                                                                                           |
| `true_text`, `false_text`            | `boolean` with text display: what prints for `true` and `false`.                                                                                                                                                                                                                                      |

**Check** (`display_type: "check"`) and **shape** (`display_type: "shape"`): a check mark or shape prints when a
`boolean` is `true` (`invert_boolean_condition: true` prints it for `false` or no value), when a `string` or `number`
matches `condition`, and for other types when there's a value. A `static` one always prints.

| Setting                                                        | Values                                                                                                                                                                                                                                                             |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `condition`                                                    | The value a `string` or `number` is compared with.                                                                                                                                                                                                                 |
| `string_condition_type`                                        | `equals` (default), `contains`, `starts_with`, `ends_with`, `regex` (RE2 syntax without lookarounds, `\p` classes or `\B`; the error says what to change), each with a `not_` form (`not_contains`, `not_regex`, ...); `blank` and `not_blank` ignore `condition`. |
| `number_condition_type`                                        | `equals` (default), `gt`, `gte`, `lt`, `lte`, `range` (with `number_condition_range_min`, `number_condition_range_max` and their `_exclusive_` settings).                                                                                                          |
| `check_character`                                              | `&#10004;` (✔, default), `&#10003;` (✓), `&#10006;` (✖), `&#10007;` (✗), `&#10008;` (✘).                                                                                                                                                                         |
| `check_color`                                                  | 6 hex digits.                                                                                                                                                                                                                                                      |
| `shape_type`                                                   | `square` (default), `rectangle`, `circle`, `ellipse`, `triangle`, `polygon` (`shape_sides` 3 to 12).                                                                                                                                                               |
| `shape_fill_color`, `shape_border_color`, `shape_border_width` | Colors in hex; the border in whole points.                                                                                                                                                                                                                         |

**Image** (`image`, `signature`, `initials`): `image_scale_type` is `fit` (default), `fill` or `stretch` (image fields
only: signatures always fit); `image_gravity` is `Center` (default), `North`, `NorthEast`, `East`, `SouthEast`,
`South`, `SouthWest`, `West` or `NorthWest`.

**QR code** (`qrcode`): `qrcode_color`. **Barcode** (`barcode`): `barcode_symbology`.

Colors can come from the data: `color_field_name` (and `background_color_field_name`, `check_color_field_name`,
`qrcode_color_field_name`, `shape_fill_color_field_name`, `shape_border_color_field_name`) names a data field whose hex
value sets the color for each submission.

Every setting, its type and default: [field schema](https://docspring.com/docs/reference/field-schema/) and
[field defaults](https://docspring.com/docs/reference/field-defaults/).

## 5. Recipes

Positions are left out of these for brevity: every field needs `page`, `x`, `y`, `width` and `height`.

**Checkbox** (ticked when `true`):

```json
{
  "name": "agrees_to_terms",
  "type": "boolean",
  "display_type": "check",
  "width": 45,
  "height": 45
}
```

**Radio group** (one of several boxes): one `string` field per box, all with the same name, `display_type` `check`,
and each box's own `condition`. `option_list` (shared) lists the choices:

```json
[
  {
    "name": "tax_classification",
    "type": "string",
    "display_type": "check",
    "option_list": "Individual,C Corporation,S Corporation",
    "condition": "Individual",
    "string_condition_type": "equals"
  },
  {
    "name": "tax_classification",
    "type": "string",
    "display_type": "check",
    "condition": "C Corporation"
  },
  {
    "name": "tax_classification",
    "type": "string",
    "display_type": "check",
    "condition": "S Corporation"
  }
]
```

The data sends `"tax_classification": "C Corporation"`. Use the option text people will read: forms show it as a
select list. More: [radio buttons](https://docspring.com/docs/template-editor/radio-buttons/).

**Several boxes that can all be ticked**: separate `boolean` check fields grouped by name, such as `services/cleaning`
and `services/repairs`, so the data is `{"services": {"cleaning": true, "repairs": false}}`.

**Signature and initials**: `type` `signature` (or `initials`), `display_type` `image`, in a box that covers the
signing line and the space above it (900 × 200 units in the docs' example). The signature is scaled to fit the box.
Signers fill these in through signature requests: see the `docspring-signature-requests` skill. A test PDF can send
`{"text": {"name": "Jane Doe", "typeface": "Dancing Script"}}`.

**A date split into day, month and year boxes**: three fields named `date_of_birth`, `type` `date`, with
`date_time_format` `%d`, `%m` and `%Y` (`%-d` and `%-m` drop the leading zero).

**SSN or other boxes with one character each**: three fields named `ssn` with `comb: true`, `comb_number_of_cells` 3,
2 and 4, and `comb_value_offset` 0, 3 and 5. One value, `"123456789"`, fills all three.
More: [SSN and comb fields](https://docspring.com/docs/template-editor/ssn-fields/).

**Text over several printed lines**: `multiline: true` with `multiline_lines` set to the number of lines on the form,
or one field per line named `notes#0`, `notes#1`, `notes#2`.

**Combined value** (printed from other fields):

```json
{
  "name": "full_name",
  "type": "combined",
  "combined_field_names": "first_name,last_name",
  "combined_field_type": "separator",
  "combined_field_separator": " "
}
```

`combined_field_type: "format"` with `combined_field_format: "$0, $1"` places the values in text instead. Make the
source fields `hidden: true` if they shouldn't print on their own.

**Fixed text or mark on every PDF**: `static: true` with the text in `default`, or a static `boolean` check field for a
box that's always ticked. Static fields aren't in the data.

**Calculated number**:

```json
{
  "name": "total",
  "type": "number",
  "default": "SUM(items.amount) * (1 + tax_rate)",
  "decimal_places": 2,
  "required": false
}
```

**QR code**: a `string`, `email` or `url` field with `display_type` `qrcode`, in a square box.

**Image** (a logo or photo): `type` `image`, `display_type` `image`. The data sends `{"url": "https://..."}` or
`{"base64": "..."}`.

## 6. Field names

- A name is the key of the field's value in the data. `/` nests it: `applicant/address/city` is
  `{"applicant": {"address": {"city": ...}}}`.
- A number segment makes a list: `dependents/0/name` and `dependents/1/name` are the first two items of `dependents`.
  The items' fields share their settings, but not their values.
- Names are case-sensitive: `firstName` and `firstname` are two fields.
- `~1` is a literal `/` and `~0` a literal `~` (JSON Pointer).
- `notes#0`, `notes#1`: one value, `notes`, split over lines of text.
- `@@date`, `@@datetime`, `@@version` and `@@data_url` print details of the submission instead of data.
  `@@signature_requests/0/completed_at` prints when the first signature request was completed.
- A field with no name gets no data and is left out of the data schema.
- Prefer lowercase snake_case segments without spaces or dots (`applicant/first_name`). Formulas read `.` as nesting,
  and names with spaces need braces in formulas.

More: [field names](https://docspring.com/docs/template-editor/field-names/).

## 7. Conditional logic

A rule has an `action`, `conditions`, and `match` (`all`, the default, or `any`):

- `require_and_show`: the fields show, and are required, only when the conditions match.
- `show`: the fields show only when the conditions match. A field whose own `required` is set is required when shown.
- `require`: the fields always show, and are required only when the conditions match.

Each condition has a `field` (a name), an `operator` and, for most operators, a `value`:

| `operator`               | `value`                                                |
| ------------------------ | ------------------------------------------------------ |
| `present`, `blank`       | None                                                   |
| `equals`, `not_equals`   | A string, number or boolean                            |
| `in`                     | A list                                                 |
| `gt`, `gte`, `lt`, `lte` | A number; the field must be a `number` field           |
| `range`                  | `value` (low end) and/or `range_max`; a `number` field |

A field's own rule is its `dependencies` (set it with `update_fields`):

```json
{
  "id": 12,
  "dependencies": {
    "action": "require_and_show",
    "conditions": [
      { "field": "marital_status", "operator": "equals", "value": "Married" }
    ]
  }
}
```

The template's rules are `field_dependencies` (set with `update_template`), each with the `targets` it applies to.
`update_template` replaces the whole list, so start from the list `get_template` returns:

```json
{
  "field_dependencies": [
    {
      "action": "require_and_show",
      "match": "all",
      "conditions": [
        { "field": "has_dependents", "operator": "equals", "value": true }
      ],
      "targets": ["dependents/0/name", "dependents/0/date_of_birth"]
    }
  ]
}
```

Fields a rule hides aren't required, aren't printed, and their values are ignored. A rule's source field can be
shown by another rule; a hidden source counts as blank. Formulas are calculated before rules are checked. In
signature requests, a rule can only use the sender's data and the fields of the signer it applies to.
More: [conditional logic](https://docspring.com/docs/template-editor/conditional-logic/).

## 8. Formulas

A `number` field's `default` (or a static number field's) can be a formula over other `number` fields.

- Operators: `+ - * / % ^`, a percentage `15%`, comparisons `= != < <= > >=`.
- Functions: `SUM`, `MIN`, `MAX`, `AVG`, `ABS`, `ROUND(x, 2)`, `ROUNDUP`, `ROUNDDOWN`, `IF(cond, a, b)`, `AND`, `OR`,
  `NOT`, and math functions such as `SQRT` and `LOG`.
- References: `/` in a name becomes `.` (`totals/subtotal` is `totals.subtotal`), list items are `items[0].price`,
  a column is `SUM(items.price)`, and `@price * @quantity` uses fields in the same row of a list. Names with spaces or
  punctuation go in braces: `{Unit Price}`.
- A value sent in the data is printed instead of the formula, so calculated fields must not be required.
- A formula stays blank until one of the fields it uses has a value.
- A change that leaves a formula unable to calculate (it uses a field that isn't a `number` field, or doesn't parse)
  is refused, and the error names the field.

More: [formulas](https://docspring.com/docs/template-editor/formulas/).
