## Description: <br>
UI design-style selector that helps an agent apply a user-specified design system from a bundled design-md library, including brand-inspired styles such as Linear, Apple, Stripe, and Vercel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill in Claude Code when they explicitly request a named design style, need a list of available styles, or want an existing interface restyled according to one of the bundled design-system references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The copy helper can write a DESIGN.md file into the selected target directory. <br>
Mitigation: Review the target directory before running copy-design.sh and confirm overwriting or adding DESIGN.md is intended. <br>
Risk: Preview HTML files may contact third-party font hosts when opened. <br>
Mitigation: Open previews only in environments where third-party font requests are acceptable, or replace the configured font host before use. <br>
Risk: Random or keyword-based style helpers may choose a style that the user did not explicitly select. <br>
Mitigation: Use get-design.sh or copy-design.sh with an explicit style name when exact style selection is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouchang1988/awesome-design-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zhouchang1988) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Design style index](artifact/scripts/styles.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and copied DESIGN.md files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May copy a selected DESIGN.md file into the target working directory; preview HTML assets may load fonts from third-party font hosts when opened.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
