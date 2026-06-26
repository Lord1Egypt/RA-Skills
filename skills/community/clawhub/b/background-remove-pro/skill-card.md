## Description: <br>
Bg Remove removes image backgrounds with AI models, supporting single-image and batch processing that outputs transparent PNG files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, ecommerce operators, content creators, and developers use this skill to remove backgrounds from product, portrait, and general images. It supports single-file and folder workflows, optional model selection, alpha matting, and controlled output naming for transparent PNG results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AI model may download on first use, which can introduce network access in otherwise controlled environments. <br>
Mitigation: Preload required models or use local model paths when offline or tightly controlled network behavior is required. <br>
Risk: Using --force can overwrite existing output files. <br>
Mitigation: Use explicit input and output paths and avoid --force unless overwriting is intentional. <br>
Risk: The skill depends on Python image-processing packages and writes generated files to disk. <br>
Mitigation: Install dependencies only in environments where those packages are acceptable, and review output locations before running batch jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/background-remove-pro) <br>
- [Publisher profile](https://clawhub.ai/user/SxLiuYu) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image files with transparent alpha channels, plus command-line status text and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs default to PNG files with a _nobg suffix unless configured otherwise; batch mode can preserve original base filenames.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
