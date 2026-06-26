## Description: <br>
Generates professional PowerPoint (.pptx) presentations using JSX/TSX with Deno, supporting slides, text, shapes, tables, charts, images, gradients, shadows, and flexible layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claw-bot](https://clawhub.ai/user/claw-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation authors use this skill to create PowerPoint slide decks, reports, and pitch decks from TypeScript JSX source files. It is suited for workflows where an agent drafts or edits slide code and then generates a .pptx artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install path uses a live remote shell script and depends on packages fetched from external sources. <br>
Mitigation: Install only after reviewing and trusting the Deno installer and the JSR package source used by the release. <br>
Risk: The generator runs TSX slide files with broad local read and write access. <br>
Mitigation: Run only TSX files you wrote or reviewed, use a project sandbox, and prefer path-scoped Deno permissions limited to the deck assets and intended PPTX output. <br>


## Reference(s): <br>
- [@pixel/pptx package](https://jsr.io/@pixel/pptx) <br>
- [Deno](https://deno.land) <br>
- [Corespeed](https://corespeed.io) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, JSON] <br>
**Output Format:** [TSX slide code and Deno shell commands that generate a PPTX file, with optional JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Deno and writes the requested .pptx file to the local filesystem.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
