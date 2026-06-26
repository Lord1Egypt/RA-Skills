## Description: <br>
Take full-page screenshots of local HTML files as PNG images using Chrome and puppeteer-core, with optional PDF output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cclam5](https://clawhub.ai/user/cclam5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to render locally authored HTML reports, visualizations, and shareable pages into PNG screenshots or PDF documents when a browser capture workflow is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe input handling and weak browser isolation may make untrusted HTML files or paths risky to process. <br>
Mitigation: Use this skill only with trusted local HTML files and paths, and prefer a temporary directory containing only the target file and required assets. <br>
Risk: Unexpected filenames or viewport values may affect the screenshot workflow. <br>
Mitigation: Use simple filenames and numeric viewport widths, and review command arguments before execution. <br>
Risk: The documented PDF mode may not be reliable until patched. <br>
Mitigation: Prefer PNG output for normal use and avoid relying on PDF output until the issue is fixed and reviewed. <br>


## Reference(s): <br>
- [Chrome Screenshot on ClawHub](https://clawhub.ai/cclam5/chrome-screenshot) <br>
- [Publisher profile: cclam5](https://clawhub.ai/user/cclam5) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions with bash and JSON examples; generated PNG or PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a full-page PNG screenshot; optional PDF output is documented but should be treated cautiously until reviewed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
