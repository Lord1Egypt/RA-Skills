## Description: <br>
Draws BBS compatible ANSI art via the Clawbius API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n2tr0n](https://clawhub.ai/user/n2tr0n) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Artists, developers, and agent operators use ANSIClaw to generate BBS-compatible ANSI art through a local Clawbius canvas API, including image-inspired renditions and scripted ANSI scenes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify the active Clawbius canvas and save generated ANSI or PNG files. <br>
Mitigation: Confirm the intended canvas and output path before running drawing scripts, and use versioned filenames to avoid overwriting existing work. <br>
Risk: Reference art or private input images may be processed by the agent during ANSI rendition work. <br>
Mitigation: Use only images and reference files that are appropriate for local agent processing, especially when handling private or regulated content. <br>
Risk: Opening reference ANSI files in Clawbius makes them the active canvas. <br>
Mitigation: Analyze reference files read-only, then create a fresh canvas before drawing so reference material is not modified. <br>


## Reference(s): <br>
- [Clawbius API Reference](references/api.md) <br>
- [Clawbius Project](https://github.com/n2tr0n/clawbius) <br>
- [ANSIClaw ClawHub Page](https://clawhub.ai/n2tr0n/ansiclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets and local API call instructions; generated art is saved as ANS and PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Clawbius API on 127.0.0.1:7777 and writes versioned ANSI art output files.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
