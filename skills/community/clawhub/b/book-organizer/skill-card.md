## Description: <br>
Organizes book content into structured Markdown notes, including book metadata, chapter summaries, mind maps, core concepts, selected quotes, key arguments, reflections, reviews, and knowledge frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ioygy](https://clawhub.ai/user/ioygy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent to gather book metadata and produce structured reading notes, chapter summaries, mind maps, concept tables, selected quotes, reviews, and knowledge frameworks as Markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents toward shadow e-book sources for full-book downloads. <br>
Mitigation: Use books the user owns, licensed library access, public-domain works, or user-provided files; do not allow automatic downloads from shadow e-book sites. <br>
Risk: The skill can create Markdown files in the workspace. <br>
Mitigation: Ask the agent to confirm the target filename and path before writing. <br>
Risk: Generated book metadata, summaries, quotes, and opinions can be inaccurate when source material is incomplete or unverified. <br>
Mitigation: Verify book metadata against reliable sources and label any summary based on partial information. <br>


## Reference(s): <br>
- [Output Template Reference](references/templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ioygy/book-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown files with structured sections, tables, quote blocks, and optional Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated notes to the workspace root or a books/ directory after the agent confirms the filename and path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
