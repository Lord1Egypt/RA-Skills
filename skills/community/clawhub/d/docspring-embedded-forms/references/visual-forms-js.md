# Visual Forms JS reference

`DocSpring.createVisualForm(cssSelector, optionsAndCallbacks)` renders a visual form (fields filled in on the PDF's
pages) inline, inside the element that `cssSelector` matches. PDF templates only, one form per page. Source of truth:
https://docspring.com/docs/forms/js-libraries/visual-forms-js/ (Markdown: replace the trailing slash with `.md`).
Where an option needs a minimum library version, it says so: check the version the page loads.

## Contents

- Options
- String options
- Callbacks
- Global functions
- Styling

## Options

`templateId` (a string starting with `tpl_`) is required, unless you pass `templateData`, cached template data that
saves a request.

| Option                        | Default                        | What it does                                                                                                                                                 |
| ----------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `templateVersion`             | `null`                         | The version to show and submit, such as `"1.2.3"` or `"draft"`. Default: the latest published version, or the draft if none is published.                    |
| `defaultFormData`             | `{}`                           | Values people can change, as nested submission JSON. Values the person already typed in this browser win.                                                    |
| `staticFormData`              | `{}`                           | Values people can't change in the form. The browser still sends them, so don't rely on them.                                                                 |
| `fieldOverrides`              | `{}`                           | Field settings by field name, such as `{ notes: { hidden: true } }`. From the browser, the submission keeps only `hidden`, `required` and `backgroundColor`. |
| `test`                        | `false`                        | `true` makes test submissions. A function is called on submit and returns `true` or `false` (2.15.0+).                                                       |
| `metadata`                    | `null`                         | Saved with the submission as its `metadata` (2.15.0+). The browser can change it.                                                                            |
| `redirectURL`                 | `null`                         | Where to go after submitting. Overrides the template's redirect URL.                                                                                         |
| `redirectURLQueryParams`      | `true`                         | Adds `submission_id`, `template_id` and `template_name` to the redirect URL.                                                                                 |
| `waitForPDF`                  | `true`                         | `false` shows the thank-you title as soon as the form is saved. The download button still appears, and a redirect still waits for the PDF.                   |
| `focusFirstFieldOnLoad`       | `false`                        | Focuses the first field when the form loads.                                                                                                                 |
| `showSignatureModalOnFocus`   | `false`                        | Opens the signature pad when a signature field gets focus.                                                                                                   |
| `showHeader`                  | `true`                         | Shows the header with its navigation buttons.                                                                                                                |
| `adjustHeaderOnScroll`        | `true`                         | Keeps the header at the top of the page as the page scrolls.                                                                                                 |
| `showClearButton`             | `true`                         | Shows the Clear Form button.                                                                                                                                 |
| `showTermsOfServiceLink`      | `true`                         | Shows the terms of service link.                                                                                                                             |
| `skipAgreeToTermsOfService`   | `false`                        | Skips the "agree to terms" step.                                                                                                                             |
| `termsOfServiceLabel`         | `"DocSpring Terms of Service"` | The terms link's text.                                                                                                                                       |
| `termsOfServiceURL`           | DocSpring's terms              | The terms link's URL.                                                                                                                                        |
| `allowSkippingOptionalFields` | `null`                         | `true` shows Continue once every required field is filled in; `false` goes through every field. `null` uses the template's setting (2.16.0+).                |
| `previewMode`                 | `false`                        | Shows the form with a single Close button instead of submitting.                                                                                             |
| `previewModeButtonLabel`      | `"Close"`                      | The preview mode button's text.                                                                                                                              |
| `showPdfProcessingSpinner`    | `true`                         | Shows a spinner while the PDF is processing.                                                                                                                 |
| `downloadButtonLabel`         | `"Download PDF"`               | The download button's text.                                                                                                                                  |
| `region`                      | `US`                           | `US` or `EU`: the account's region.                                                                                                                          |
| `host`                        | `null`                         | One host for app and API requests, for single-domain Enterprise installs, such as `https://docspring.example.com`.                                           |
| `appHost`, `apiHost`          | `null`                         | Separate app and API hosts, for split-domain Enterprise installs.                                                                                            |

The form needs no API token: never put one in the page. Pages written for older versions may pass `apiTokenId` and
`apiTokenSecret`. They still work, but from 2.19.0 the form logs a deprecation warning: remove them, and have the user
create a new API token and revoke the old one, whose secret has been public. Get a private submission's PDF on the
server instead (`onSave` gives the page the submission ID to send it).

A field that is Static in the template ignores `defaultFormData` and `staticFormData` and shows the template's value,
which the PDF prints.

## String options

A string, or a function that returns one, for the header's titles and messages and the footer (2.12.0+). They are HTML:
escape anything a person typed.

| Option                     | Function arguments        | Shown                                         |
| -------------------------- | ------------------------- | --------------------------------------------- |
| `pdfProcessingTitle`       | `template`                | Title while the PDF is processing             |
| `pdfProcessingMessage`     | `template`                | Message while the PDF is processing           |
| `completedTitle`           | `template`, `downloadURL` | Title when the PDF is ready                   |
| `completedTitleNoDownload` | `template`                | Title when the form is submitted, no download |
| `pdfProcessedMessage`      | `template`, `downloadURL` | Message when the PDF is ready                 |
| `footerHTML`               | `template`                | A footer under the form                       |

## Callbacks

| Callback                     | Arguments                            | When                                                                                                                  |
| ---------------------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| `onInitialize`               | none                                 | The form has been set up                                                                                              |
| `onLoad`                     | none                                 | Every page image has loaded                                                                                           |
| `onClearForm`                | none                                 | The form was cleared                                                                                                  |
| `onFieldFocus`               | `{ id, name, value }`                | A field gets focus                                                                                                    |
| `onFieldBlur`                | `{ id, name, value }`                | A field loses focus                                                                                                   |
| `onFieldChange`              | `{ id, name, value, previousValue }` | A field's value changes                                                                                               |
| `onShowAcceptTerms`          | none                                 | The "accept terms" step is shown                                                                                      |
| `onSubmit`                   | `formData`                           | The form is submitted. The return value is ignored: it can't cancel.                                                  |
| `onSave`                     | `submissionId`                       | The submission is saved                                                                                               |
| `onProcessed`                | `{ submissionId, downloadURL }`      | The PDF is ready (Submission Privacy public only). A redirect follows one second later (2.12.0+).                     |
| `onError`                    | `error`, then a form error object    | Saving failed, the PDF couldn't be generated, or the template couldn't load (`{ error: 'failed_request', response }`) |
| `onPreviewModeButtonClicked` | none                                 | The preview mode button is clicked                                                                                    |

## Global functions

They act on the page's one visual form.

| Function                              | What it does                                                                                                              |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `DocSpring.clearForm()`               | Clears the values and goes back to the defaults                                                                           |
| `DocSpring.submitForm()`              | Submits, showing validation errors if there are any                                                                       |
| `DocSpring.focusNextField()`          | Focuses the next field                                                                                                    |
| `DocSpring.focusField(nameOrId)`      | Focuses a field by name or numeric ID                                                                                     |
| `DocSpring.setField(nameOrId, value)` | Sets a field's value                                                                                                      |
| `DocSpring.getFormData()`             | The values entered, as nested submission data, without defaults, static values or formula results (2.15.0+)               |
| `DocSpring.setFormData(data)`         | Replaces the values entered. Fields that `data` leaves out go back to their defaults; static fields keep theirs (2.15.0+) |
| `DocSpring.returnToForm()`            | Goes back to the form after it was submitted                                                                              |

## Styling

The form is always light, whatever the page's theme. Target `.dsp-formWrapper`, `.dsp-fieldWrapper`, `.dsp-button`,
`.dsp-primaryButton`, `.dsp-headerWrapper` and `.dsp-footerWrapper`. Template settings also give required fields their
own highlight (**Required Field Color**). The form scales itself for small screens: don't scale it with CSS transforms.
