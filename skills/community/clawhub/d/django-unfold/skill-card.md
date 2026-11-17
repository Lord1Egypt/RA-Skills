## Description:

Expert guidance for building advanced Django admin interfaces with django-unfold, including setup, ModelAdmin customization, theming, actions, filters, tabs, inlines, dashboards, and common pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ijmadalena](https://clawhub.ai/user/ijmadalena)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement, customize, and debug Django admin interfaces built with django-unfold. It helps produce installation steps, configuration guidance, Django admin code, UI customization patterns, and operational cautions for Unfold-backed admin panels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated admin actions may change orders, payments, or other business records if copied directly into production.

Mitigation: Add explicit Django permissions, confirmations, audit logging, idempotency, and tests before enabling mutating admin actions.

Risk: Dependency and frontend asset examples may drift from the target project's supported Python, Django, django-unfold, npm, or Tailwind versions.

Mitigation: Pin Python and npm dependencies with lockfiles, confirm the project's Django and django-unfold version compatibility, and run collectstatic and frontend builds in a staging environment.

Risk: Examples are implementation patterns rather than hardened production code.

Mitigation: Treat generated snippets as starting points and review authentication, authorization, validation, query performance, and error handling before deployment.

## Reference(s):

- [Installation & Setup Reference](artifact/references/installation.md)
- [Configuration Reference](artifact/references/configuration.md)
- [Theming Reference](artifact/references/theming.md)
- [Actions Reference](artifact/references/actions.md)
- [Filters Reference](artifact/references/filters.md)
- [Tabs Reference](artifact/references/tabs.md)
- [Inlines Reference](artifact/references/inlines.md)
- [Dashboard & Components Reference](artifact/references/dashboard-components.md)
- [Django Unfold Skill Page](https://clawhub.ai/ijmadalena/skills/django-unfold)
- [Publisher Profile](https://clawhub.ai/user/ijmadalena)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Python, Django template, CSS, JavaScript, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for django-unfold projects; generated examples require project-specific review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
