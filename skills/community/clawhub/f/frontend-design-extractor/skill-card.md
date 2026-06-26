## Description: <br>
Extract reusable UI/UX design systems from frontend codebases: design tokens, global styles, components, interaction patterns, and page templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xsir0](https://clawhub.ai/user/Xsir0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to extract or create reusable UI/UX specifications from frontend projects, including design tokens, global styles, component catalogs, interaction patterns, page templates, accessibility notes, and migration plans while keeping business logic out of scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect frontend source files and write UI/UX specification files into the target repository. <br>
Mitigation: Install and run it only in repositories where source inspection and a ui-ux-spec output folder are acceptable; review generated documentation before sharing or committing it. <br>
Risk: Refactor workflows may lead to UI-only code or style changes that affect product behavior or accessibility if accepted without review. <br>
Mitigation: Review proposed plans and diffs before accepting changes, and keep business logic, APIs, routing, and domain workflows unchanged. <br>
Risk: The artifact references helper scripts that may be unavailable in this release. <br>
Mitigation: Treat script-based scanning and skeleton generation as optional; if scripts are unavailable, use manual inspection and write the requested UI/UX outputs directly. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Xsir0/frontend-design-extractor) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, implementation notes, refactor plans, and optional code or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default documentation output is organized under ui-ux-spec/ unless the user requests a different layout.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
