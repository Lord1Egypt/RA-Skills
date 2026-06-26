## Description: <br>
Generates dot-line ASCII text art for terminal banners, converting Chinese input to pinyin before rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaosai](https://clawhub.ai/user/xiaosai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks for terminal banner text, ASCII art, or CLI text art. The skill extracts the requested text, optionally converts Chinese characters to pinyin, and returns dot-line terminal output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a bundled local Python script to render terminal output. <br>
Mitigation: Review the artifact before installation and run only the documented dotline_art.py command with intended user-provided text. <br>
Risk: Long or mixed-symbol input can produce hard-to-read terminal banners because unsupported characters are ignored or replaced. <br>
Mitigation: Keep requested banner text short and review the rendered output before using it in scripts, documentation, or demos. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaosai/dotline-art) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text terminal output with an optional shell command invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese input may be transliterated to pinyin; very long text can reduce terminal readability.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
