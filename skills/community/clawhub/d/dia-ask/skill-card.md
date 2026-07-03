## Description: <br>
Dia Ask prompts The Browser Company's Dia browser from the command line to read or research logged-in or JavaScript-heavy pages and return the assistant's answer as an exact text file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[germankovacevic-lab](https://clawhub.ai/user/germankovacevic-lab) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Dia Ask to delegate read and research prompts to a locally running Dia browser when pages require a logged-in browser session or heavy JavaScript rendering. It is intended for gathering exact text outputs, not for taking browser actions such as clicking or submitting forms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool requires Accessibility control over Dia from the invoking terminal or IDE. <br>
Mitigation: Install and run it only in environments where granting that local Accessibility permission is approved. <br>
Risk: Prompts and page content are processed by the user's local Dia assistant and may include sensitive or regulated data. <br>
Mitigation: Avoid secrets and regulated data unless Dia is approved for that data and the user is authorized to process it there. <br>
Risk: The fallback sender can briefly steal focus and uses clipboard-style UI automation. <br>
Mitigation: Use the focus-safe v2 sender by default and pass --no-fallback when focus stealing or clipboard interaction is unacceptable. <br>
Risk: Generated answer files can persist sensitive content on disk. <br>
Mitigation: Review where Dia writes outputs and delete generated files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/germankovacevic-lab/skills/dia-ask) <br>
- [Dia browser](https://www.diabrowser.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; command output is an absolute file path to Dia's generated text, Markdown, JSON, or CSV file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Node.js 18 or newer, Dia installed locally, and Accessibility permission for the invoking terminal or IDE.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
