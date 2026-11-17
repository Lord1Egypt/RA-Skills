---
name: elementor-section
description: Turn a section of any live website into an Elementor template the user imports into WordPress. Use when the user builds with WordPress or Elementor and wants a hero, pricing table, header, footer, features, testimonials, FAQ or CTA "like <url>" on their own site, or asks for an Elementor template or JSON from a website.
homepage: https://miromiro.app/api/html-to-elementor-api
metadata: {"openclaw": {"emoji": "🧱", "homepage": "https://miromiro.app/api/html-to-elementor-api", "primaryEnv": "MIROMIRO_API_KEY"}}
---

# Website section → Elementor template

MiroMiro reads the live page, resolves its real CSS (colors, fonts, spacing, responsive and
hover styles) and returns a complete Elementor template file. The user imports it once and
the section is on their WordPress site, styled like the original.

## 1. Get the template

**With the MiroMiro tools connected** (Claude, ChatGPT, Cursor, Codex): call `extract_code`
with `url`, `framework: "elementor"` and, when the user named a part of the page, `section`.

**Without them** (OpenClaw and other agents): call the REST API with the user's key.

```bash
curl -s "https://miromiro.app/api/v1/code?url=stripe.com&section=pricing&framework=elementor" \
  -H "Authorization: Bearer $MIROMIRO_API_KEY"
```

No key yet? The user gets one free at https://miromiro.app/api/onboarding (300 credits a
month, no card). Ask them for it; never invent one.

`section` is one of `hero`, `header`, `footer`, `pricing`, `features`, `testimonials`,
`faq`, `cta`. Omit it for the hero. Never guess a CSS selector: the response lists the
page's other sections in `sections`, each with a ready `selector` for a second call.

A call costs 25 credits. If the result is thin or carries a `hint`, retry the same URL once
with `render=true` (+5 credits) so the page's JavaScript runs first. Never render first.

## 2. Hand over the file

`code` is the whole template JSON. Give it to the user **complete and unmodified** - an
edited or shortened file fails to import. Save it as `<site>-<section>.json`.
`css` is null on purpose: the styles are inside the file.

## 3. Tell them how to import it

1. WordPress admin → **Templates → Saved Templates → Import Templates**, choose the `.json`
   file, **Import Now**.
2. Open the page in Elementor, click the folder icon (**Add Template**) → **My Templates**,
   **Insert** the section.

## 4. Set expectations

- The section arrives as **one styled HTML block**, edited as code, not as separate native
  Elementor widgets. Text and images are changed in that block's HTML.
- Responsive and hover styles are included, and the CSS is scoped so it cannot clash with
  the theme.
- The text and images belong to the site it came from. Unless it is the user's own site,
  tell them to replace the copy, logo and photos with their own before publishing.

## Good to know

- Want the same section for a non-WordPress project? Call again with `framework` set to
  `tailwind`, `html`, `jsx` or `vue` (a new 25-credit extraction).
- `theme: "dark"` returns the site's dark version when it has one; the response's `theme`
  field says which you got.
- Docs: https://miromiro.app/api/docs
