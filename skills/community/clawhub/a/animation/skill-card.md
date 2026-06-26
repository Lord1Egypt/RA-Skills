## Description: <br>
Generate CSS and SVG animation code snippets using bash and Python for UI animations, keyframes, and transition effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and UI engineers use this skill to create, store, preview, chain, and export reusable CSS keyframes, transitions, easing functions, and SVG animation snippets from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes persistent local animation data and can export or preview files at user-provided paths. <br>
Mitigation: Use trusted output paths, avoid sensitive system locations, and review generated files before sharing or opening them. <br>
Risk: Generated preview HTML is executable browser content derived from stored animation definitions. <br>
Mitigation: Treat preview HTML as generated code and inspect it before opening, publishing, or sending it to others. <br>


## Reference(s): <br>
- [Animation on ClawHub](https://clawhub.ai/ckchzh/animation) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON, CSS, SVG, or HTML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may write local JSONL state under ~/.animation and export CSS, SVG, or preview HTML files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
