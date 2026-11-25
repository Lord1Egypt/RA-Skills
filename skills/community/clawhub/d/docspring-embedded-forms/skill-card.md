## Description:

Puts DocSpring forms and the template editor in a browser. Sets up hosted form links, embedded web forms (DocSpring.createWebForm) and visual forms (DocSpring.createVisualForm) with prefill, hidden fields, callbacks, redirects, styling and the public template settings they need, upgrades Web Forms JS 2.x (createSimpleForm), and embeds the template editor (DocSpring.createTemplateEditor, embed_edit_token). Use when the user wants people to fill in a DocSpring template on their site or from a link, wants their own users to edit templates in their product, or has code loading web_form, simple_form, visual_form or template_editor from cdn.docspring.com. Not for e-signatures or embedded signing (docspring-signature-requests), server-side PDF generation or webhooks (docspring-api-integration), or other form builders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docspring](https://clawhub.ai/user/docspring)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to configure hosted or embedded DocSpring forms and template editors in browser based products. It helps them choose an integration, wire its JavaScript and page settings, and handle submissions and privacy safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public forms accept unauthenticated submissions, which can consume account credits.

Mitigation: Treat the template ID as public, monitor submissions, and route sensitive or authoritative submissions through server-side validation.

Risk: Prefills, hidden fields, metadata, and other form values come from the browser and can be changed by visitors.

Mitigation: Validate values on the server before relying on them for prices, identity, or other consequential decisions.

Risk: Public submission privacy can allow anyone with a submission ID to download its PDF.

Mitigation: Keep submissions private when they contain personal data and retrieve PDFs on the server.

Risk: Personal data placed in hosted form URLs can appear in browser history and logs.

Mitigation: Avoid putting personal data in form links; send it through a protected application flow instead.

Risk: An API token exposed in front-end code can grant access to the DocSpring account.

Mitigation: Keep API tokens in server-side environment variables and send the browser only the data it needs.

## Reference(s):

- [Web Forms JS reference](artifact/references/web-forms-js.md)
- [Visual Forms JS reference](artifact/references/visual-forms-js.md)
- [Template editor reference](artifact/references/template-editor.md)
- [Compare DocSpring forms](https://docspring.com/docs/forms/compare-docspring-forms/)
- [Embedded web forms guide](https://docspring.com/docs/guides/embedded-forms/embedded-web-forms.md)
- [Embedded visual forms guide](https://docspring.com/docs/guides/embedded-forms/embedded-visual-forms.md)
- [Embedded template editor guide](https://docspring.com/docs/guides/embedded-template-editor.md)
- [Web Forms JS changelog](https://docspring.com/docs/changelogs/web-forms-js.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with JavaScript, HTML, CSS, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Integration-specific examples and safety guidance]

## Skill Version(s):

1.9.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
