## Description: <br>
Provides a Chinese Asakusa Temple omikuji experience that draws a real numbered fortune, presents the poem and explanations, and offers one ritual redraw only when the first lot is unfavorable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaozrrr](https://clawhub.ai/user/shaozrrr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to draw a Chinese Asakusa Temple fortune slip and receive ceremonial prose with the sign number, auspiciousness, poem, explanation, and an optional one-time redraw for unfavorable results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the helper downloads and runs unpinned remote Python code from GitHub, so later upstream changes could alter local behavior without a ClawHub package update. <br>
Mitigation: Review before installing or running; prefer a version that bundles the fortune data and drawing code locally, or pins and verifies any remote content and avoids executing downloaded Python. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaozrrr/asakusa-omikuji-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted Chinese prose with fortune fields and optional shell command execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs a single fortune-reading flow, with redraw guidance limited to unfavorable lots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
