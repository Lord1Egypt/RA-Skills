## Description: <br>
Colorpick helps agents convert color formats, generate palettes and harmonies, check contrast, and produce terminal-oriented color guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use Colorpick to convert HEX, RGB, and HSL values, generate palette ideas, find complementary colors, and check WCAG contrast in shell-based design or CSS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Colorpick may persist user-provided command inputs in local history and export files. <br>
Mitigation: Do not enter secrets, private prompts, client names, filenames, or internal design notes unless local persistence is acceptable. <br>
Risk: Search and export behavior may expose previously saved colorpick inputs beyond the immediate command session. <br>
Mitigation: Review generated local data before sharing exports, and prefer an isolated data directory when evaluating the skill. <br>
Risk: The security scan reports that persistence is not clearly scoped or disclosed. <br>
Mitigation: Require clear documentation, opt-in logging, configured data-directory handling, export fixes, and a purge command before broad deployment. <br>


## Reference(s): <br>
- [Colorpick ClawHub listing](https://clawhub.ai/ckchzh/colorpick) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local history and export files when the bundled shell wrapper is used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
