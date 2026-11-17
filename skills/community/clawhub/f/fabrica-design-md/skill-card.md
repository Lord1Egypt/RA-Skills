## Description:

Fabrica Design Md helps an agent extract a user's existing visual identity from code, screenshots, or interview answers, measure contrast, and deliver a DESIGN.md plus a measured proof page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, business owners, and developers use this skill to document a real brand visual system for reuse by AI coding or design agents. It is intended for extracting an identity from existing successful pieces, code, screenshots, or interview answers rather than inventing a new brand.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand screenshots, private ZIP files, and generated DESIGN.md content may include sensitive business or visual identity information.

Mitigation: Use trusted transfer and storage locations, avoid sending unnecessary private assets, and review the generated DESIGN.md before reusing it in other skills.

Risk: The artifact includes behavior that can allow copying a known brand if the user insists.

Mitigation: Use the extraction workflow on the user's own materials, avoid the copy-known-brand exception, and remove any copied brand values during review.

Risk: Playwright or Chromium installation and page measurement may execute browser tooling in the local environment.

Mitigation: Approve browser installation only in a trusted environment and inspect generated HTML before running measurement commands.

## Reference(s):

- [plantilla-design-md.md](references/plantilla-design-md.md)
- [contraste.py](references/contraste.py)
- [medir.mjs](references/medir.mjs)
- [ClawHub skill release page](https://clawhub.ai/formula100k/skills/fabrica-design-md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, guidance]

**Output Format:** [Markdown files, an HTML proof page, screenshots, shell commands, and concise final guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces DESIGN.md, prueba.html, measured desktop and mobile screenshots when tooling is available, and reported contrast ratios from the bundled script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
