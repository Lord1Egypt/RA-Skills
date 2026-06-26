## Description: <br>
Generates professional PowerPoint (.pptx) presentations from JSX/TSX slide files with Deno, supporting slides, text, shapes, tables, charts, images, gradients, shadows, and flexible layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zypher-agent](https://clawhub.ai/user/zypher-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create presentation decks, pitch decks, reports, and other PPTX files by writing a TSX slide definition and running the included Deno generator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator imports and runs TSX slide files as executable code with local read and write access. <br>
Mitigation: Use slide files created for the current task or otherwise trusted, and scope Deno permissions to the specific input, asset, and output paths where possible. <br>
Risk: The published install metadata recommends a curl-to-shell Deno installer command. <br>
Mitigation: Install Deno through a trusted package manager or verify the installer source before running it. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/zypher-agent/corespeed-slide) <br>
- [@pixel/pptx package](https://jsr.io/@pixel/pptx) <br>
- [Deno install](https://deno.land/install.sh) <br>
- [Corespeed](https://corespeed.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with TypeScript/TSX snippets, shell commands, optional JSON command output, and generated .pptx files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Deno and executes user-provided TSX slide files to produce PPTX output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
