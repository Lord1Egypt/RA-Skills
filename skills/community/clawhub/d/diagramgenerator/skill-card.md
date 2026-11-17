## Description:

Generates and iteratively edits Mermaid.js and Draw.io diagrams with multimodal context from source code, architecture sketches, and documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaudata](https://clawhub.ai/user/kaudata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate or revise Mermaid and Draw.io diagrams from prompts, existing diagram code, source files, documentation, PDFs, or images. It supports architecture, flowchart, ER, Gantt, Git graph, and similar diagramming workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web server is unauthenticated and can use the user's Gemini key or manage saved files.

Mitigation: Run it only on a trusted local machine, avoid exposing port 3000, and add authentication plus local-only binding before broader deployment.

Risk: Prompt context may include source code, documents, PDFs, or images that are sent for Gemini processing.

Mitigation: Do not upload secrets or confidential code unless approved, and enforce the documented allowlist and blocklist before attaching files.

Risk: Browser dependencies and viewers are loaded from external URLs and saved outputs are served from the local downloads path.

Mitigation: Pin or bundle browser dependencies where possible, review saved artifacts before sharing, and document retention and deletion expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaudata/skills/diagramgenerator)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Mermaid browser renderer](https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs)
- [diagrams.net viewer](https://viewer.diagrams.net/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request payloads and shell commands; generated diagrams are Mermaid text or Draw.io XML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Node.js server, GEMINI_API_KEY, curl, and base64; the web UI can export .mmd, .drawio, .png, and .jpg files.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
