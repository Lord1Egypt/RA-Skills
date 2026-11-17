## Description:

Front-end design skill for building React UIs with Ant Design (antd): component patterns, layout, forms, tables, and theming/tokens via ConfigProvider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipeoff](https://clawhub.ai/user/felipeoff)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to build React and Ant Design v5 application screens with consistent layouts, forms, tables, CRUD flows, theming, accessibility checks, and runnable code outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runnable starter may include outdated npm build dependencies before installation or dev server use.

Mitigation: Audit and update starter dependencies before running npm install, npm run dev, or npm run build.

Risk: Generated UI examples may be adapted to destructive actions or real backend search/upload flows without adequate user safeguards.

Mitigation: Keep delete confirmations, verify locale-specific behavior, and clearly disclose real backend search or upload behavior in adapted applications.

Risk: The skill assumes Ant Design v5 token theming, which can produce incorrect guidance for Ant Design v4 projects.

Mitigation: Confirm the project uses Ant Design v5 before applying token guidance; for v4, pause and choose an upgrade or v4 Less-variable theming path.

## Reference(s):

- [Ant Design Documentation](https://ant.design/)
- [Ant Design GitHub Repository](https://github.com/ant-design/ant-design)
- [Ant Design v5 Tokens Cookbook](references/tokens.md)
- [Ant Design React Page Recipes](references/components.md)
- [UI Spec Protocol](protocols/UI_SPEC.md)
- [Output Contract](protocols/OUTPUT_CONTRACT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with file tree sections, full file contents, run commands, assumptions, and TypeScript or TSX code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs should include exact install, dev, and build commands and should pass TypeScript build checks; audit and update starter dependencies before running npm install or a dev server.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
