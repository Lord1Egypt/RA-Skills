## Description: <br>
Convert colors and generate palettes with WCAG contrast checks. Use when building palettes, converting hex/RGB, checking accessibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and accessibility reviewers use Colorlab to convert hex and RGB colors, generate lighter or darker palette variants, check WCAG contrast ratios, and find nearby CSS color names from a local command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local shell script, so users could be exposed to unexpected behavior if they install a modified copy from an untrusted source. <br>
Mitigation: Install only the reviewed Colorlab release from a trusted publisher and compare release hashes or ClawHub security status when available. <br>
Risk: Color and palette outputs can be misleading if users pass malformed color values or rely on limited named-color matching for design decisions. <br>
Mitigation: Use normal hex/RGB/count inputs, review command output before applying it, and treat closest CSS color names as approximate labels. <br>


## Reference(s): <br>
- [Colorlab on ClawHub](https://clawhub.ai/bytesagain3/colorlab) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text with ANSI color swatches and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local color and count inputs; palette swatches require a modern terminal with ANSI 24-bit color support.] <br>

## Skill Version(s): <br>
3.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
