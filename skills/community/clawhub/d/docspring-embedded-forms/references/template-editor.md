# Embedded template editor reference

`DocSpring.createTemplateEditor(selector, options)` loads the template editor in an iframe. Source of truth:
https://docspring.com/docs/guides/embedded-template-editor/,
https://docspring.com/docs/guides/embedded-template-editor/customize-embedded-template-editor/ and
https://docspring.com/docs/guides/embedded-template-editor/use-predefined-fields/ (Markdown: replace the trailing slash
with `.md`).

## Contents

- Calling it
- Options
- Events
- Features
- Capabilities
- Predefined fields
- Version attribution

## Calling it

- `createTemplateEditor('#editor', options)`: inline, filling the element (unless `inline: false`).
- `createTemplateEditor(options)`: a modal over the page. `options.selector` can name the element instead.
- It throws `templateId and token are required!` without both.
- It returns `{ iframe, close, url }`. `close()` (or `DocSpring.closeTemplateEditor()`) removes the iframe and its
  message listener and calls `onClose`. A new editor closes the previous one first. A modal closes itself after
  `onDone` and `onEvent` run.

## Options

| Option                                       | Default                | What it does                                                                                                 |
| -------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------ |
| `templateId`                                 | required               | The template's ID (`tpl_...`).                                                                               |
| `token`                                      | required               | The template's `embed_edit_token`, fetched by the server.                                                    |
| `externalUser`                               | none                   | `{ name, email, external_id }`: labels changes and published versions. Without it: "Embedded Template User". |
| `selector`                                   | none                   | The element for an inline editor, instead of the first argument.                                             |
| `inline`                                     | `true` with a selector | `false` opens a modal even with a selector.                                                                  |
| `darkMode`                                   | stored or system theme | `true` forces the dark theme, `false` the light one.                                                         |
| `showDoneButton`                             | `true`                 | Shows the Done button in the editor's header.                                                                |
| `doneButtonLabel`                            | `"Done"`               | The Done button's text.                                                                                      |
| `disableDoneButtonIfPredefinedFieldsMissing` | `true`                 | Keeps Done disabled until every `required_in_template` predefined field is on the template.                  |
| `features`                                   | see below              | Shows or hides editor controls.                                                                              |
| `closeModalOnClickOverlay`                   | `true`                 | Modal: a click on the overlay closes the editor.                                                             |
| `fullScreenModal`                            | `false`                | Modal: uses the window's full width (by default it's 500px narrower above 767px).                            |
| `modalMaxWidth`                              | none                   | Modal: a CSS length such as `1200px` or `80vw`.                                                              |
| `iframeClass`, `iframeStyle`                 | none                   | Extra classes and inline CSS for the iframe.                                                                 |
| `editorURL`                                  | generated              | Overrides the iframe URL (local development, custom routing). Messages are checked against its origin.       |
| `region`                                     | `US`                   | `US` or `EU`.                                                                                                |
| `host`, `appHost`, `apiHost`                 | none                   | Enterprise hosts: one host for both, or separate ones.                                                       |

The inline iframe is `width: 100%; height: 100%; min-height: 640px`, so the container sets its height.

## Events

Each callback gets an object with the `templateId`, plus:

| Callback           | Data                                    | When                                                                                                 |
| ------------------ | --------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `onLoad`           |                                         | The editor has loaded                                                                                |
| `onSave`           |                                         | A change was saved to the draft                                                                      |
| `onDocumentUpdate` |                                         | A replacement PDF was saved                                                                          |
| `onVersionPublish` | `version`                               | A version was published (versioning capability only)                                                 |
| `onVersionRestore` | `version`                               | A version was restored to the draft (versioning capability only)                                     |
| `onVersionDelete`  | `version`                               | A version was deleted (versioning capability only)                                                   |
| `onDone`           | `missingPredefinedFields`               | Done was clicked: only with no unsaved changes, no save running and no save error                    |
| `onError`          | `message`, `status`, sometimes `errors` | A save failed. `errors` lists problems with the template, such as a formula that can't be calculated |
| `onClose`          | none                                    | The editor closed, including by `close()` or a new editor                                            |
| `onEvent`          | `(eventName, data)`                     | Every event above except `onClose`                                                                   |

## Features

Pass `features: { ... }` to show or hide controls. These are cosmetic: see Capabilities for the real limits.

| Feature                      | Default | Shows                                                                        |
| ---------------------------- | ------- | ---------------------------------------------------------------------------- |
| `showSettings`               | `true`  | The settings panel. Needs `embed_edit_allow_settings`.                       |
| `showVersions`               | `true`  | Version publishing, restore and delete. Needs `embed_edit_allow_versioning`. |
| `allowPdfReplacement`        | `true`  | Uploading a new PDF. Needs `embed_edit_allow_document_replacement`.          |
| `showSchema`                 | `true`  | The JSON schema button                                                       |
| `showFormSections`           | `true`  | The Sections button (the web form's sections)                                |
| `showCode`                   | `false` | The Code button (model code for the template's data)                         |
| `showFormLinks`              | `true`  | Links to the hosted form pages                                               |
| `showHelp`                   | `true`  | The help link                                                                |
| `showInvert`                 | `true`  | The Invert button for PDFs in dark mode                                      |
| `showNewFieldTypePicker`     | `true`  | The toolbar's field type picker                                              |
| `showPredefinedFields`       | `true`  | Predefined field controls                                                    |
| `showWelcomeModal`           | `true`  | The welcome modal, each time the editor loads                                |
| `showTemplateDefaultOptions` | `true`  | The template's default field settings                                        |
| `showFieldDataType`          | `true`  | Field data type controls                                                     |
| `showFieldRequired`          | `true`  | The Required checkbox                                                        |
| `showFieldHidden`            | `true`  | Hidden field controls                                                        |
| `showFieldStatic`            | `true`  | Static field controls                                                        |
| `showFieldDefaultValue`      | `true`  | Default value controls                                                       |
| `showFieldInfo`              | `true`  | Field title and description                                                  |
| `showFieldRotation`          | `true`  | Rotation                                                                     |
| `showFieldOpacity`           | `true`  | Opacity                                                                      |
| `showFieldConditions`        | `true`  | Conditional display                                                          |
| `showFieldDependencies`      | `true`  | Conditional logic (show, hide or require a field based on others)            |
| `showFieldQrBarcode`         | `true`  | QR code and barcode options                                                  |
| `showFieldDateOptions`       | `true`  | Date and time formats                                                        |
| `showFieldMetadata`          | `true`  | Field metadata                                                               |
| `showFieldFontAdvanced`      | `true`  | Advanced font controls                                                       |
| `showFieldValidation`        | `true`  | Validation, such as length limits                                            |
| `showFieldCombOptions`       | `true`  | Comb fields                                                                  |
| `showFieldColorFromData`     | `true`  | Colors from submitted data                                                   |

`simplifyUI: true` sets these to `false`: `showSchema`, `showFormSections`, `showCode`, `showFormLinks`, `showHelp`, `showInvert`,
`showWelcomeModal` and every `showField...` switch except `showFieldDataType` and `showFieldRequired`. Other switches in
the same object override it, such as `{ simplifyUI: true, showFieldRotation: true }`.

## Capabilities

Template settings, all `false` by default, set with `update_template` (`PUT /templates/{template_id}`) or in the
dashboard. The server enforces them, and turns the matching feature off when one is `false`.

| Setting                                 | Lets the embed                                                                            |
| --------------------------------------- | ----------------------------------------------------------------------------------------- |
| `embed_edit_allow_settings`             | See and change settings: webhook and redirect URLs, encryption, public access, expiration |
| `embed_edit_allow_versioning`           | Publish, restore, compare and delete versions                                             |
| `embed_edit_allow_document_replacement` | Upload a replacement PDF                                                                  |

Without `embed_edit_allow_settings`, the editor gets sensitive settings (webhook URLs, the redirect URL, encryption
passwords) as `null` or safe defaults. With any settings, the token can't change Embed Domains or the capabilities, lock
the template, regenerate its token, copy the template, or delete the draft or the whole template.

## Predefined fields

Set `predefined_fields` with `update_template` (`PUT /templates/{template_id}`). It replaces the whole list; an empty
list turns predefined fields off.

```json
{
  "predefined_fields": [
    { "name": "customer/name", "type": "string", "required_in_template": true },
    {
      "name": "customer/email",
      "type": "email",
      "required_in_template": true,
      "field_required": true
    },
    {
      "name": "requiredInfo_name",
      "display_name": "Defendant/Name",
      "title": "Defendant Name",
      "type": "string"
    }
  ]
}
```

| Property               | Required | What it does                                                                                                                           |
| ---------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                 | yes      | The key in submission data. `/` nests it: `customer/email`, `signers/0/name`.                                                          |
| `type`                 | yes      | `string`, `number`, `boolean`, `date`, `address`, `country`, `email`, `url`, `image`, `signature`, `initials`, `barcode` or `combined` |
| `display_name`         | no       | What the editor shows instead of `name`; a `/` puts it in a folder. Two names can't share one.                                         |
| `title`                | no       | The Title a field gets when it's given this name                                                                                       |
| `option_list`          | no       | String fields only: allowed values, comma-separated, such as `"Yes,No"`                                                                |
| `required_in_template` | no       | The template must have a field with this name (default `false`). Drives the missing list and the Done button.                          |
| `field_required`       | no       | The Required setting a field gets with this name (default `true`)                                                                      |

`predefined_fields_sample_data` builds the list from sample submission data instead: each value becomes a field with a
type that fits it and `required_in_template: true`. To keep fields' Required setting from the list, hide the checkbox
with `features: { showFieldRequired: false }`.

## Version attribution

The template's published `versions` say who published each one: `published_by_type` (`user` or `external_user`),
`published_by_user_id` (`usr_...`, for DocSpring users), `published_by_external_id` (your `externalUser.external_id`),
`published_by_name` and `published_by_email`.
