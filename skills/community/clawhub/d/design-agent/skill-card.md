## Description: <br>
Design consultation skill for AI agents that provides structured design prompts, DESIGN.md files, color systems, typography rules, spacing conventions, and component patterns for visual output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[defineagain](https://clawhub.ai/user/defineagain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and other agents use this skill to turn visual-output requests into reusable design guidance, including tokens, DESIGN.md content, component patterns, and review checklists for UI, HTML, newsletters, PDFs, and related artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated design files or guidance may be written to an unintended location or may introduce incorrect visual standards. <br>
Mitigation: Review any generated DESIGN.md or design guidance, confirm the target path before writing, and verify the result before relying on it. <br>
Risk: Screenshot-based visual review can expose confidential or sensitive UI content to a vision model. <br>
Mitigation: Avoid sending confidential screenshots to vision review, or redact sensitive information before review. <br>
Risk: The skill references third-party design sites and npx commands that may change over time. <br>
Mitigation: Verify third-party sites and commands before opening links or running shell commands. <br>


## Reference(s): <br>
- [Design Tokens - Base System](references/design-tokens.md) <br>
- [Integration Guide - How Other Skills Call design-agent](references/integration-guide.md) <br>
- [Design Prompt Template](assets/design-prompt-template.md) <br>
- [design-extractor.com](https://www.design-extractor.com) <br>
- [typeui.sh](https://www.typeui.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with design tokens, checklists, code blocks, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose writing DESIGN.md files and may request screenshot-based visual review before final sign-off.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
