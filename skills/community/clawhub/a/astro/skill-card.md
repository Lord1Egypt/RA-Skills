## Description:

Deploy multilingual static websites on Cloudflare with Astro using markdown sources, supporting i18n, free hosting, and Git-based or direct deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bezkom](https://clawhub.ai/user/bezkom)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create Astro static sites or blogs, configure multilingual content, and deploy the resulting site to Cloudflare Pages. It also provides helper scripts for creating localized Markdown posts and checking translation coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The post-creation helper can create Markdown files outside the intended content folder when given crafted language, title, or path-like inputs.

Mitigation: Use trusted inputs, validate language codes and generated slugs, and confirm created paths stay inside the intended content directory before relying on generated files.

Risk: Astro and Cloudflare commands may change local project state or deploy public site content.

Mitigation: Review commands before execution, run them in a trusted project checkout, and prefer pinned or local versions of Astro and Wrangler.

## Reference(s):

- [ClawHub Astro skill page](https://clawhub.ai/bezkom/skills/astro)
- [Astro Docs](https://docs.astro.build)
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages)
- [Astro i18n Guide](https://docs.astro.build/en/guides/i18n/)
- [Astro Cloudflare Adapter](https://docs.astro.build/en/guides/deploy/cloudflare/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks and shell command examples; helper scripts produce text reports, JSON reports, or Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper scripts use the Python standard library and operate on local project files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
