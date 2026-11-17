---
name: drin-build-template
description: Build a transactional HTML email that renders correctly across Gmail, Outlook, and Apple Mail, with a plain-text alternative and dark-mode support. Use when writing or editing the HTML/text body of an email, or creating a reusable Drin template with variables. Covers the table-based layout rules, inlined styles, bulletproof buttons, preheader, and Drin's {{handlebars}} variable/section syntax.
version: 1.0.0
---

# Building cross-client transactional email

Email clients are not browsers. Outlook uses Word to render HTML; Gmail strips
`<style>` in some contexts and clips messages over ~102KB; many clients block
external CSS and JS. Build defensively.

## Hard rules

1. **Layout with tables, not flexbox/grid.** Use nested `<table>` with
   `role="presentation"`, `cellpadding="0" cellspacing="0" border="0"`.
2. **Inline every style** (`style="…"` on elements). Treat `<style>` blocks as a
   progressive enhancement only (use for `@media` dark mode / mobile).
3. **Fixed width ≤ 600px** for the main column; make it fluid on mobile.
4. **Always ship a plain-text part.** Never send HTML-only — it hurts
   deliverability and breaks for text-only readers. Drin takes `text` alongside
   `html`.
5. **A preheader**: a hidden span right after `<body>` that sets the inbox
   preview line.
6. **Bulletproof buttons**: a styled `<a>` inside a padded table cell (not a
   `<button>`), with VML for Outlook if you need a filled button there.
7. **Alt text on every image**; assume images are blocked by default. Don't put
   critical content only in an image.
8. **No JavaScript, no `<form>` you depend on, no web fonts you depend on**
   (provide a system-font fallback stack).
9. **Dark mode**: set `color-scheme`/`supported-color-schemes: light dark` and
   provide `@media (prefers-color-scheme: dark)` overrides; don't rely on them —
   pick colors that survive auto-inversion.

## Starter skeleton

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="color-scheme" content="light dark" />
    <meta name="supported-color-schemes" content="light dark" />
    <title>{{subject | default:"Notification"}}</title>
    <style>
      @media (prefers-color-scheme: dark) {
        .bg { background:#0b0b0c !important; }
        .card { background:#161617 !important; }
        .text { color:#e7e7e7 !important; }
        .muted { color:#a1a1a1 !important; }
      }
    </style>
  </head>
  <body class="bg" style="margin:0; padding:0; background:#f4f4f5;">
    <!-- preheader: shown in the inbox preview, hidden in the body -->
    <div style="display:none; max-height:0; overflow:hidden; opacity:0;">
      {{preheader | default:"A quick update from {{brandName}}"}}
    </div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td align="center" style="padding:24px 12px;">
          <table role="presentation" class="card" width="600" cellpadding="0" cellspacing="0" border="0"
                 style="max-width:600px; width:100%; background:#ffffff; border-radius:12px;">
            <tr>
              <td class="text" style="padding:32px; font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif; font-size:15px; line-height:1.6; color:#18181b;">
                <h1 style="margin:0 0 16px; font-size:20px;">Hi {{firstName | default:"there"}},</h1>
                <p style="margin:0 0 24px;">{{body}}</p>
                <!-- bulletproof button -->
                <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                  <tr>
                    <td align="center" bgcolor="#2563eb" style="border-radius:8px;">
                      <a href="{{ctaUrl}}" style="display:inline-block; padding:12px 22px; font-family:Arial,sans-serif; font-size:15px; color:#ffffff; text-decoration:none;">
                        {{ctaLabel | default:"Open"}}
                      </a>
                    </td>
                  </tr>
                </table>
                <p class="muted" style="margin:24px 0 0; font-size:12px; color:#71717a;">
                  Sent by {{brandName}}. {{#if unsubscribeUrl}}<a href="{{unsubscribeUrl}}" style="color:#71717a;">Unsubscribe</a>.{{/if}}
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
```

Always produce a matching plain-text version, e.g.:

```
Hi {{firstName | default:"there"}},

{{body}}

{{ctaLabel | default:"Open"}}: {{ctaUrl}}

Sent by {{brandName}}.
```

## React Email (TypeScript)

If the project sends from TypeScript, prefer [react-email](https://react.email)
components and render with the Drin SDK helper:

```ts
import { sendReactEmail } from "@drin00/sdk/react-email";
await sendReactEmail(drin, { from, to, subject, react: <Welcome name="Ada" /> });
// renders html + text, then sends
```

## Drin's {{handlebars}} template syntax

When you save a reusable template in Drin (`create_template` / `POST /v1/templates`
/ dashboard), the engine is a **safe handlebars subset** — no arbitrary code,
purpose-built for email:

- `{{ path }}` — HTML-escaped interpolation (use in the HTML body).
- `{{{ path }}}` or `{{& path }}` — raw/unescaped (use sparingly, e.g. pre-sanitized HTML).
- `{{ path | default:"x" }}`, `{{ path | upper }}`, `{{ path | lower }}` — filters.
- `{{#if path}} … {{else}} … {{/if}}`, `{{#unless path}} … {{/unless}}`.
- `{{#each items}} … {{this}} / {{@index}} / {{@first}} / {{@last}} … {{else}} … {{/each}}`.
- `{{../x}}` — parent scope; `{{! comment }}` — stripped.

Missing variables render as empty string and are reported. Before sending, call
`render_template` (a saved template) or `preview_template` (an unsaved draft;
`templates.preview` in the SDK) and check the `missing` array — fix any required
variable that resolved to empty. The **subject** and **text** parts render
unescaped; the **html** part is escaped by default.
