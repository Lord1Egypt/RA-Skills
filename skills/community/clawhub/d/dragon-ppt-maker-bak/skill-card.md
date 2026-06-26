## Description: <br>
Dragon Ppt Maker.Bak helps agents create styled PowerPoint presentations with python-pptx, including title, content, feature grid, comparison, image, and HTML-preview slides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huayang0704](https://clawhub.ai/user/huayang0704) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate polished PPTX presentations from command-line arguments or Python API calls, with built-in themes and reusable slide layouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The OpenClaw demo mode saves to a built-in Desktop-style output path. <br>
Mitigation: Prefer passing an explicit --output path for normal use and avoid --openclaw when that hard-coded path is not appropriate. <br>
Risk: Generated presentations may include user-supplied text, image paths, or HTML snippets. <br>
Mitigation: Review provided content and local file paths before generation; the HTML helper stores a text preview rather than executing embedded HTML. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huayang0704/dragon-ppt-maker-bak) <br>


## Skill Output: <br>
**Output Type(s):** [files, code, shell commands, guidance] <br>
**Output Format:** [PPTX file output with optional Python API examples and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script accepts a title, pipe-delimited content, output path, theme, and an OpenClaw demo mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
