## Description: <br>
Draw is a local Bash design journal for recording palettes, previews, generated asset notes, conversions, contrast checks, gradients, swatches, searches, and exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers and front-end developers use Draw to keep a local color and design activity journal, including palette entries, contrast notes, gradients, swatches, and exportable design history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as an SVG diagram generator, but the security summary says it mainly stores user-entered design text in local logs. <br>
Mitigation: Use it only as a local design/color journal unless the implementation is separately reviewed and verified for SVG generation behavior. <br>
Risk: Design entries are stored in plaintext under ~/.local/share/draw and may be searched or exported later. <br>
Mitigation: Do not enter secrets, proprietary prompts, client names, sensitive filenames, or private URLs; review generated exports before sharing them. <br>


## Reference(s): <br>
- [Draw on ClawHub](https://clawhub.ai/bytesagain3/draw) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text stdout with optional JSON, CSV, or TXT exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries in plaintext local files under ~/.local/share/draw.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
