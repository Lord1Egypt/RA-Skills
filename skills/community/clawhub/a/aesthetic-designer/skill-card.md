## Description: <br>
A Chinese-first aesthetic design assistant that helps agents create design concepts, style matrices, palettes, visual AI prompts, and design critiques using art and design movements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyucheneureka](https://clawhub.ai/user/xuyucheneureka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, developers, and creative agents use this skill to turn visual design requests into structured concepts, aesthetic direction, color palettes, material notes, and prompts for visual AI tools. It is also useful for lightweight design critique and art-direction brainstorming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The critique helper can produce generic critique rather than grounded analysis of the supplied design. <br>
Mitigation: Treat critique output as brainstorming support and have a human reviewer validate design-specific feedback before relying on it. <br>
Risk: Broad activation triggers and Chinese-first behavior may route visual design requests to this skill when a different language or narrower design workflow is desired. <br>
Mitigation: Use activation or language preference rules when installing the skill in environments that need narrower routing. <br>


## Reference(s): <br>
- [Aesthetic Matrix](references/aesthetic-matrix.md) <br>
- [Color Theory](references/color-theory.md) <br>
- [Prompt Engineering](references/prompt-engineering.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured design sections, tables, palettes, prompts, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are primarily Chinese-first design guidance; helper scripts can emit markdown design skeletons, palettes, and critiques.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
