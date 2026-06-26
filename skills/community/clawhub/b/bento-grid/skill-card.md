## Description: <br>
Generate beautiful bento grid layouts for social media posts, including Instagram and Twitter cards with statistics, calendars, music visualization, and custom layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limoxt](https://clawhub.ai/user/limoxt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and social media operators use this skill to generate Python/Pillow snippets for square bento grids, statistics cards, and music-listening cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The examples run local Python snippets with Pillow and write fixed filenames under /tmp, which can overwrite existing temporary image files with the same names. <br>
Mitigation: Review snippets before execution and change output filenames or paths when preserving existing /tmp files matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/limoxt/bento-grid) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated snippets save PNG image files to /tmp, including bento_grid.png, stats_card.png, and music_card.png.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
