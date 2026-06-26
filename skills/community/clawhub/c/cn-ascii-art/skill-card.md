## Description: <br>
Converts user-provided text into ASCII art using pyfiglet when available, with a simple uppercase fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators can use this skill to generate ASCII-art renderings of short text for terminal output, signatures, examples, or lightweight decorative text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may install or run the skill without reviewing local file access, credentials, external service usage, or background behavior. <br>
Mitigation: Inspect the skill files and requested permissions during installation, following the supplied clawscan guidance. <br>
Risk: ASCII-art output can vary or degrade when pyfiglet is unavailable or when a requested font is unsupported. <br>
Mitigation: Install pyfiglet when consistent rendering is required and verify the selected font with representative text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-ascii-art) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text ASCII art and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output quality depends on pyfiglet availability and the requested font.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
