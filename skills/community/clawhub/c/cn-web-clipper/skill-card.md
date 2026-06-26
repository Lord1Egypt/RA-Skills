## Description: <br>
Cn Web Clipper fetches a user-provided webpage, extracts readable article text and metadata, and saves the clipping as a local Markdown file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to clip web articles into local Markdown notes from URLs they provide. It is suited to personal knowledge capture, article archiving, and lightweight research workflows where local files are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided URLs and can save extracted content from sensitive internal or private pages. <br>
Mitigation: Use it only with URLs intended for clipping, and choose a dedicated output folder for saved Markdown files. <br>
Risk: Repeated clips with the same date and title can produce the same Markdown filename. <br>
Mitigation: Review the output path before relying on a saved clip, and rename or separate outputs when clipping multiple similar pages. <br>


## Reference(s): <br>
- [Cn Web Clipper ClawHub page](https://clawhub.ai/freedompixels/cn-web-clipper) <br>
- [freedompixels publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown files with plain-text CLI status and optional JSON result output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes extracted webpage content to a local output directory selected by CLI argument or environment variable.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
