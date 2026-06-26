## Description: <br>
Generates and iteratively edits Mermaid.js and Draw.io diagrams. Supports multimodal context (reading source code, architecture sketches, and documentation). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaudata](https://clawhub.ai/user/kaudata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate, revise, preview, and export Mermaid or Draw.io diagrams from prompts, source files, documentation, PDFs, and sketches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts and attached files are sent to Gemini for diagram generation. <br>
Mitigation: Attach only non-secret, non-confidential files and avoid sending credentials, environment files, private repositories, or sensitive business data. <br>
Risk: Saved diagram outputs are managed by an unauthenticated local web server. <br>
Mitigation: Run the server locally, avoid exposing port 3000 to other users or networks, and periodically delete saved diagrams that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaudata/diagramgenerator) <br>
- [Mermaid.js Runtime](https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs) <br>
- [diagrams.net Viewer](https://viewer.diagrams.net/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions and API payloads that produce Mermaid code, Draw.io XML, and exported diagram files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated diagrams may be saved locally as .mmd, .drawio, .png, or .jpg files.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
