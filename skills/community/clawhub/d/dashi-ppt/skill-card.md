## Description:

制作 PPT、演示文稿、幻灯片、汇报材料时使用。Dashi PPT 基于预置视觉主题组合页面,生成可离线打开、可在浏览器编辑的 HTML 演示,支持导出 PPTX / PDF 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[haixiandaxia-jpg](https://clawhub.ai/user/haixiandaxia-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, analysts, consultants, and developers use this skill to turn a natural-language presentation request into an offline HTML slide deck, with optional PPTX or PDF export. It is suited for report, pitch, research, and business presentation workflows that need selectable visual themes and editable browser previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Previewed decks may be exposed on the local network without authentication.

Mitigation: Set DASHI_PPT_PREVIEW_HOST=127.0.0.1 before rendering and avoid confidential decks unless LAN exposure is fixed.

Risk: Preview server processes may keep running after generation.

Mitigation: Stop preview server processes after use.

Risk: Installation and rendering may download npm or Playwright dependencies and perform a remote update check.

Mitigation: Review the package before installation and run it only in environments where those network and dependency actions are acceptable.

Risk: Browser preview and editing can create local editing state.

Mitigation: Use the skill only for decks you are comfortable previewing on the machine where it runs.

## Reference(s):

- [Current Options](references/options.md)
- [Layout Roles](references/layout-roles.md)
- [Goal Spec Schema](references/goal-spec.schema.json)
- [Portfolio Example](references/examples/portfolio.json)
- [Annual Review Example](references/examples/annual-review.json)
- [Dashi PPT Project Homepage](https://github.com/chuspeeism/dashi-ppt-skill)
- [ClawHub Skill Page](https://clawhub.ai/haixiandaxia-jpg/skills/dashi-ppt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with JSON plans and shell commands; generated decks are HTML files with optional PPTX or PDF exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm; first use may install dependencies and use a local browser preview service.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter and package.json report 0.4.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
