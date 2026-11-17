## Description:

Element UI Vue2 helps agents provide Vue 2 desktop UI guidance using Element components for forms, tables, dialogs, navigation, layout, theming, and related component APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufengsheng](https://clawhub.ai/user/wufengsheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when building Vue 2.x desktop web pages with Element UI components and when they need quick access to component usage, API attributes, events, slots, methods, installation, theming, and internationalization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency and CDN snippets may be copied without fixed versions or integrity controls.

Mitigation: Pin npm and CDN versions, use project lockfiles, and add subresource integrity for browser-loaded assets where practical.

Risk: UI examples for upload, dynamic HTML, and form validation can be mistaken for production security controls.

Mitigation: Add server-side file validation, sanitize or escape user-controlled HTML, and enforce server-side validation for sensitive actions.

Risk: The reference set is mainly zh-CN documentation and may need localization review for teams working in other languages.

Mitigation: Have implementers confirm translated terminology and component behavior against the project requirements before applying examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wufengsheng/skills/element-ui-vue2)
- [Element UI Chinese documentation](https://element.eleme.cn/#/zh-CN)
- [Element UI installation guide](https://element.eleme.cn/#/zh-CN/component/installation)
- [Element UI changelog](https://element.eleme.cn/#/zh-CN/component/changelog)
- [Element UI GitHub releases](https://github.com/ElemeFE/element/releases)
- [Skill definition](artifact/SKILL.md)
- [Installation reference](artifact/references/dev-guide/installation.md)
- [Component reference bundle](artifact/llms-full.txt)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Vue, JavaScript, HTML, CSS, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily zh-CN Element UI Vue 2 reference material; users should review generated examples before production use.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
