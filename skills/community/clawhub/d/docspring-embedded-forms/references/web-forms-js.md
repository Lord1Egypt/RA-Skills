# Web Forms JS reference

`DocSpring.createWebForm(selector, templateId, options)` renders a web form (form fields on a page) for a PDF or HTML
template inside the element that `selector` matches (a CSS selector or the element itself). The form replaces what's
in the element. It throws when nothing matches, and returns nothing. Source of truth:
https://docspring.com/docs/forms/js-libraries/web-forms-js/ (Markdown: replace the trailing slash with `.md`).

This is Web Forms JS 3.x (`embed/web_form.v3.*`). Pages on 2.x (`embed/simple_form.v2.*`, `createSimpleForm`) differ
in `onError` and styling: see "Upgrading from 2.x" in https://docspring.com/docs/changelogs/web-forms-js/.

## Contents

- Options
- Globals
- Callbacks
- Errors
- Success screen
- Redirects
- Sections
- Styling
- Hosted web form query params

## Options

| Option                        | Default                | What it does                                                                                                                                                                                   |
| ----------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `templateVersion`             | none                   | The version to show and submit, such as `"1.2.3"` or `"draft"`. Default: the latest published version, or the draft if none is published.                                                      |
| `defaultData`                 | `{}`                   | Values for the fields, as nested submission JSON. Values the person already typed in this browser win (see SKILL.md, "Saved progress beats prefill").                                          |
| `metadata`                    | `{}`                   | Saved with the submission. In API responses and webhooks, not in the PDF. The browser can change it.                                                                                           |
| `showButtons`                 | `true`                 | `false` hides both buttons.                                                                                                                                                                    |
| `showClearButton`             | `true`                 | `false` hides the Clear button.                                                                                                                                                                |
| `showSubmitButton`            | `true`                 | `false` hides the submit button.                                                                                                                                                               |
| `clearButtonLabel`            | `"Clear"`              | The Clear button's text.                                                                                                                                                                       |
| `submitButtonLabel`           | `"Submit Form"`        | The submit button's text.                                                                                                                                                                      |
| `submitButtonSavingLabel`     | `"Saving..."`          | The submit button's text while saving.                                                                                                                                                         |
| `submitButtonProcessingLabel` | `"Generating PDF..."`  | The submit button's text while waiting for the PDF.                                                                                                                                            |
| `redirectURL`                 | none                   | Where to go after submitting. Overrides the template's redirect URL; `null` doesn't clear it.                                                                                                  |
| `waitForPDF`                  | `true`                 | `false` stops waiting for the PDF once the form is saved: it redirects straight away (if there's a redirect URL) and doesn't call `onProcessed`. No effect when Submission Privacy is private. |
| `showSuccessScreen`           | `true`                 | `false` keeps the form on the page once it's submitted (as 2.x did) instead of showing the success screen.                                                                                     |
| `successTitle`                | the template's setting | The success screen's title.                                                                                                                                                                    |
| `successMessage`              | the template's setting | The success screen's message, as plain text. `""` shows none.                                                                                                                                  |
| `showFillAgainButton`         | the template's setting | Whether the success screen has a Fill out again button.                                                                                                                                        |
| `sectionList`                 | `'left'`               | Where a form with sections lists them: `'left'` beside the form (above it when the form is narrower than 720px), or `'top'` above it.                                                          |
| `sectionsInOrder`             | the template's setting | Whether a form with sections keeps later sections locked until the visitor reaches them with Next.                                                                                             |
| `theme`                       | none                   | Custom property values without the `--dsp-` prefix: `{ primary: '#0b6e4f', radius: '4px' }` (see Styling).                                                                                     |
| `darkMode`                    | `false`                | `true` for the dark theme, `'auto'` to follow the visitor's system setting.                                                                                                                    |

There is no `test` option: embedded web forms always make live submissions. There is no `region` option either.

## Globals

Set these on `window.DocSpring` before calling `createWebForm`:

- `DocSpring.appHost`: the app host, without a scheme. `'app-eu.docspring.com'` for EU accounts; an Enterprise
  install's own host.
- `DocSpring.scheme` (default `'https'`) and `DocSpring.port`: for Enterprise or local installs.

## Callbacks

| Callback                | Arguments    | When                                                                                                                                          |
| ----------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `processTemplateSchema` | `jsonSchema` | Before the form renders. Change the schema in place (or return a new one): delete a property (and its entry in `required`) to hide a field.   |
| `onClearForm`           | none         | When the Clear button is pressed.                                                                                                             |
| `onSubmit`              | `formData`   | When the submit button is pressed and every answer is valid. Return `false` to cancel the submission.                                         |
| `onSave`                | `submission` | When the submission is saved. Has `id`.                                                                                                       |
| `onProcessed`           | `submission` | When the PDF is ready. Only when Submission Privacy is public and `waitForPDF` isn't `false`. The redirect, if any, follows one second later. |
| `onSuccess`             | `submission` | Kept from 2.x: when the PDF is ready, just before `onProcessed`, with the same submission. Use `onProcessed`.                                 |
| `onError`               | `error`      | On any error (below).                                                                                                                         |

The `submission` object has `id`, `state` (`"pending"`, `"processed"`), `download_url` and `expires_at` (both `null`
until the PDF is processed).

## Errors

`onError` gets `{ error, message }`, plus `status` (the HTTP status, when there was a response), `errors` (the API's
messages) and `submission` where they apply:

- `failed_request`: the template couldn't be loaded (for example, Online Form Privacy is private), the form couldn't be
  saved, or a request for the PDF's status failed.
- `invalid_data`: the API rejected the data. The form also shows the errors at their fields.
- `submission_timeout`: the PDF wasn't ready within 60 seconds.
- `invalid_status`: the PDF couldn't be generated. The submission is in `submission`.

The form shows save and PDF errors above its buttons itself; `onError` is for the page's own handling.

```javascript
onError: function (error) {
  if (error.error === 'invalid_data') {
    console.error('Validation failed:', error.errors)
  } else {
    console.error(error.error, error.message)
  }
}
```

## Success screen

Once the submission is saved, the form is replaced by a success screen: a title ("Thanks for filling out" and the
template's name, by default), the template's message, a Download PDF button once the PDF is ready (Submission Privacy
public only) and a Fill out again button, which clears the form and its saved progress. The template's Forms settings
set the title, message and button; the `successTitle`, `successMessage` and `showFillAgainButton` options override
them. A form that redirects shows no success screen. To show the page's own message instead, pass
`showSuccessScreen: false` and use `onSave` or `onProcessed`.

## Redirects

The redirect URL gets `submission_id`, `template_name`, `template_version` and `template_id` query params. With
Submission Privacy private, the form redirects as soon as it saves; with it public, after the PDF is ready (unless
`waitForPDF: false`).

## Sections

A template's sections (the template editor's **Sections**, `x-form-sections` in the schema: `{ id, title, description,
properties }`) make the form show one section at a time, with Next and Back and a list of sections. The page can't
add sections except by changing `x-form-sections` in `processTemplateSchema`. Sections are versioned like fields
(SKILL.md, rule 3).

## Styling

The form draws a `.dsp-web-form` element inside the container, and its stylesheet only applies inside it. Restyle it
with CSS custom properties on `.dsp-web-form` (or the `theme` option); a rule in the page's CSS wins over the defaults
whichever stylesheet loads first:

```css
.dsp-web-form {
  --dsp-font-family: 'Inter', sans-serif;
  --dsp-primary: #0b6e4f;
  --dsp-primary-hover: #08563d;
  --dsp-radius: 4px;
}
```

The properties: `--dsp-font-family` (default: the page's font), `--dsp-font-size` (15px), `--dsp-text`,
`--dsp-text-secondary`, `--dsp-placeholder`, `--dsp-background` (transparent), `--dsp-surface`,
`--dsp-surface-sunken`, `--dsp-border`, `--dsp-input-background`, `--dsp-input-border`, `--dsp-primary`,
`--dsp-primary-hover`, `--dsp-primary-text`, `--dsp-danger`, `--dsp-danger-background`, `--dsp-success`,
`--dsp-success-background`, `--dsp-focus`, `--dsp-radius` (6px), `--dsp-control-height` (40px) and `--dsp-spacing`
(16px). The docs page's "Styling web forms" says what each one styles.

- Dark theme: `darkMode: true` or `'auto'`. The background stays transparent, so set `--dsp-background` unless the page
  is dark. For dark-only colors, target `.dsp-web-form[data-dsp-theme="dark"]` (and `[data-dsp-theme="auto"]` inside
  `@media (prefers-color-scheme: dark)`); `theme` values apply to both themes.
- Classes for other rules start with `dsp-`: `.dsp-field`, `.dsp-label`, `.dsp-input`, `.dsp-button-submit`,
  `.dsp-button-clear` and so on. The submit and Clear buttons keep 2.x's `.alpaca-form-button-submit` and
  `.alpaca-form-button-clear`; no other `.alpaca-*` class exists.
- Logos set on the account appear on hosted forms only.

## Hosted web form query params

For links to `https://app.docspring.com/templates/<template ID>/form` (https://docspring.com/docs/forms/web-forms/):

| Param                   | Example                                                                    |
| ----------------------- | -------------------------------------------------------------------------- |
| `data[<field>]`         | `data[name]=John%20Smith`                                                  |
| nested and array fields | `data[person][name]`, `data[person][][name]`                               |
| `metadata[<key>]`       | `metadata[userId]=123`, `metadata[pdf_filename]=Invoice_123`               |
| `hidden_fields`         | `hidden_fields=name,person/0/name` (field names as in the template editor) |
| `version`               | `version=1.2.3`                                                            |
| `mode`                  | `web`, `visual` or `dual`                                                  |

The visual form can't hide fields, so a link with `hidden_fields` shows the web form unless it also has `mode=visual`.
